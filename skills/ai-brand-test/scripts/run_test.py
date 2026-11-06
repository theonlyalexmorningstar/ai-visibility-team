"""Ask buyer questions to ChatGPT and Gemini (their live web apps), Google's AI Overview, Google AI Mode,
Claude and Perplexity, all through one treg.to key, and save every answer with the websites it cited.
Stdlib only. MIT, Alex Andronov.

Usage: python3 run_test.py "<test folder>" [--limit N]
Reads numbered questions from <test folder>/questions.md; writes answers.jsonl there.
Key: TREG_API_KEY env var, or the file ~/.config/treg/key. Country: COUNTRY env var (default US).
Cost: about $0.025 per question for all six (a 20-question test is about $0.50).
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

KEY = os.environ.get("TREG_API_KEY") or open(os.path.expanduser("~/.config/treg/key")).read().strip()
COUNTRY = os.environ.get("COUNTRY", "US").upper()


def treg(path, body=None, query=None, tries=3):
    """One treg call. Returns (json, cost_usd, error)."""
    url = "https://treg.to/call/" + path + ("?" + urllib.parse.urlencode(query) if query else "")
    for i in range(tries):
        req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method="POST" if body else "GET",
                                     headers={"X-Treg-Token": KEY, "Content-Type": "application/json", "X-Treg-Route-Max-Cost": "0.05"})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r), int(r.headers.get("X-Treg-Cost-Micro", 0) or 0) / 1e6, None
        except Exception as e:
            err = str(e); time.sleep(3 * (i + 1))
    return {}, 0.0, err


def domain(u):
    return re.sub(r"^www\.", "", re.sub(r"^https?://", "", u or "").split("/")[0].split("#")[0])


def ask_cloro(app, q):  # the live ChatGPT / Gemini web interface
    j, cost, err = treg(f"cloro.ai-search.{app}.scrape", {"prompt": q, "country": COUNTRY, "include": {"markdown": True}})
    res = j.get("result") or {}
    sites = [domain(s.get("url")) for s in (res.get("citationPills") or []) + (res.get("sources") or [])]
    return res.get("markdown") or res.get("text") or "", sites, cost, err


def ask_ai_overview(q):  # Google AI Overview on a normal search; retried once because it doesn't always load
    total = 0.0
    for _ in range(2):
        j, cost, err = treg("litescrape.google.serp.ai_overview", query={"q": q, "gl": COUNTRY.lower(), "hl": "en"})
        total += cost
        ao = (j.get("result", j) or {}).get("ai_overview") or {}
        def texts(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k in ("snippet", "title") and isinstance(v, str): yield v
                    elif k != "references": yield from texts(v)
            elif isinstance(o, list):
                for v in o: yield from texts(v)
        text = "\n".join(texts(ao.get("text_blocks", [])))
        if text or err: break
    return text, [domain(x.get("link")) for x in ao.get("references", [])], total, err or (None if text else "no AI Overview shown")


def ask_ai_mode(q):  # Google AI Mode (its answer comes without a source list)
    j, cost, err = treg("crawl4ai.google.serp.ai_mode", query={"q": q, "deep": "0", "gl": COUNTRY.lower(), "hl": "en"})
    text = (j.get("answer") or {}).get("text") or ""
    return text, [], cost, err or (None if text else j.get("note") or "no AI Mode answer")


def ask_llm(se, model, q):  # Claude and Perplexity through their APIs (via DataForSEO); prompts are capped at 500 characters
    j, cost, err = treg(f"dataforseo.x.ai-optimization-{se}-llm-responses-live",
                        [{"user_prompt": q[:500], "model_name": model, "web_search": True, "max_output_tokens": 1500}])
    res = ((j.get("tasks") or [{}])[0].get("result") or [{}])[0]
    secs = [s for it in res.get("items") or [] for s in it.get("sections") or []]
    text = "\n".join(s.get("text") or "" for s in secs).strip()
    sites = [domain(a.get("url")) for s in secs for a in s.get("annotations") or []]
    return text, sites, cost, err or (None if text else (j.get("tasks") or [{}])[0].get("status_message") or "no answer")


ASSISTANTS = {"ChatGPT": lambda q: ask_cloro("chatgpt", q), "Gemini": lambda q: ask_cloro("gemini", q),
              "Google AI Overview": ask_ai_overview, "Google AI Mode": ask_ai_mode,
              "Claude": lambda q: ask_llm("claude", "claude-sonnet-4-5", q),
              "Perplexity": lambda q: ask_llm("perplexity", "sonar", q)}


def run_one(job):
    qn, group, q, label = job
    text, sites, cost, err = ASSISTANTS[label](q)
    return {"q": qn, "group": group, "question": q, "assistant": label, "country": COUNTRY, "date": time.strftime("%Y-%m-%d"),
            "answer": text, "cited_sites": list(dict.fromkeys(s for s in sites if s)), "cost": cost, "error": err}


def questions(folder):
    out, group = [], ""
    for line in open(os.path.join(folder, "questions.md")):
        g = re.match(r"\*\*([A-Z])\.", line)
        if g: group = g.group(1)
        m = re.match(r"(\d+)\. (.+\?)\s*$", line)
        if m: out.append((int(m.group(1)), group, m.group(2)))
    return out


if __name__ == "__main__":
    folder = sys.argv[1]
    qs = questions(folder)
    if "--limit" in sys.argv:
        qs = qs[: int(sys.argv[sys.argv.index("--limit") + 1])]
    assert qs, "no numbered questions found in questions.md"
    jobs = [(n, g, q, a) for n, g, q in qs for a in ASSISTANTS]
    with ThreadPoolExecutor(6) as ex:
        rows = list(ex.map(run_one, jobs))
    with open(os.path.join(folder, "answers.jsonl"), "w") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} answers, {sum(1 for r in rows if r['error'])} errors, cost ${sum(r['cost'] for r in rows):.3f}")
