"""Count which brands each saved answer names: share of answers, first mentions, broad vs specific, cited sites.
Usage: python3 analyze.py "<test folder>" "<your brand>"
Brands come from <test folder>/brands.txt, one per line; spelling variants after "|", e.g. "HubSpot|HubSpot CRM".
Re-run any time after editing brands.txt: it reads the saved answers and costs nothing. MIT, Alex Andronov.
"""
import collections, json, os, re, sys


def load_brands(folder):
    out = []
    for line in open(os.path.join(folder, "brands.txt")):
        names = [n.strip() for n in line.split("|") if n.strip()]
        if names:
            # names of 3 letters or fewer match only with their exact capitals, so they don't hit ordinary words
            alts = [re.escape(n) if len(n) > 3 else f"(?-i:{re.escape(n)})" for n in names]
            out.append((names[0], re.compile(r"(?<![\w-])(" + "|".join(alts) + r")(?![\w-])", re.I)))
    return out


# Note: a short brand that is also a common word still counts at the start of a sentence; check those by hand.
def named(text, brands):
    """Brands in the order they first appear in the answer."""
    hits = [(m.start(), b) for b, rx in brands for m in [rx.search(text)] if m]
    return [b for _, b in sorted(hits)]


def main(folder, focus):
    brands = load_brands(folder)
    rows = [json.loads(l) for l in open(os.path.join(folder, "answers.jsonl"))]
    ok = [r for r in rows if r["answer"] and not r["error"]]
    for r in ok:
        r["b"] = named(r["answer"], brands)
    neutral = [r for r in ok if focus.lower() not in r["question"].lower()]
    out = []; p = out.append
    p(f"Answers: {len(ok)} of {len(rows)} ({len(rows) - len(ok)} empty or failed). Questions that don't name {focus}: {len(neutral)} answers.")

    def share(rs, title):
        if not rs: return
        c = collections.Counter(b for r in rs for b in r["b"])
        first = collections.Counter(r["b"][0] for r in rs if r["b"])
        p(f"\n## {title} — {len(rs)} answers\n| Brand | Named in | Share | First-named |\n|---|---|---|---|")
        for b, n in c.most_common(15):
            p(f"| {b} | {n} | {100 * n / len(rs):.0f}% | {first[b]} |")

    share(neutral, "All questions")
    share([r for r in neutral if r["group"] == "A"], "Broad questions (group A)")
    share([r for r in neutral if r["group"] == "B"], "Specific needs (group B)")
    p(f"\n## {focus} by assistant\n| Assistant | Answers | Named | First |\n|---|---|---|---|")
    for a in dict.fromkeys(r["assistant"] for r in ok):
        rs = [r for r in neutral if r["assistant"] == a]
        p(f"| {a} | {len(rs)} | {sum(focus in r['b'] for r in rs)} | {sum(bool(r['b']) and r['b'][0] == focus for r in rs)} |")
    p(f"\n## Questions where {focus} was never named")
    for q in sorted({r["q"] for r in neutral}):
        rs = [r for r in neutral if r["q"] == q]
        if not any(focus in r["b"] for r in rs):
            p(f"- Q{q}: {rs[0]['question']}")
    p("\n## Websites the answers cited most")
    for s, n in collections.Counter(s for r in ok for s in r["cited_sites"]).most_common(15):
        p(f"- {s}: {n}")
    p(f"\nCost: ${sum(r['cost'] or 0 for r in rows):.3f}. Country: {rows[0].get('country', '?')}. Date: {rows[0]['date']}.")
    txt = "\n".join(out)
    open(os.path.join(folder, "summary.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "brands.txt"), "w").write("HubSpot\nPipedrive\nZoho|Zoho CRM\nAttio\nClose|Close CRM\n")
        test = load_brands(d)
    assert named("Try ZOHO CRM, then hubspot or Pipedrive. Close the deal.", test) == ["Zoho", "HubSpot", "Pipedrive", "Close"]
    assert named("An Attio-style CRM", test) == []
    main(sys.argv[1], sys.argv[2])
