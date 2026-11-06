"""Lead-magnet poster (1080x1350) and repo banner (1280x640), rendered by headless Chrome.
python3 poster.py -> poster.png, banner.png"""
import html, pathlib, subprocess
HERE = pathlib.Path(__file__).parent
COLS = [  # (department, fill, [(skill, what it does)]) — must match README
    ("AI search", "#ffe14a", [("seo-geo", "Get cited in AI answers."), ("seo-agentic", "Ready for AI agents."),
                              ("seo-content", "Is the page worth citing?"), ("humanizer", "Text that doesn't sound AI.")]),
    ("Audit", "#cfe0ff", [("seo", "Full site analysis."), ("seo-audit", "Scored site-wide audit."), ("seo-page", "One URL, every check."),
                          ("seo-technical", "Crawl, index, speed."), ("seo-images", "Alt text, size, format.")]),
    ("Content", "#d5efc9", [("seo-plan", "Strategy by industry."), ("seo-content-brief", "Briefs that beat rivals."),
                            ("seo-competitor-pages", "“X vs Y” pages."), ("seo-programmatic", "Pages at scale."),
                            ("seo-image-gen", "Hero and social images.")]),
    ("Site and local", "#ffd6c2", [("seo-schema", "Structured data AI reads."), ("seo-sitemap", "Sitemaps that get crawled."),
                                   ("seo-hreflang", "Right page per language."), ("seo-local", "Google Business Profile."),
                                   ("seo-maps", "Map rankings by area.")]),
    ("Data", "#e4dafc", [("seo-google", "Search Console and GA4."), ("seo-backlinks", "Who links to you."),
                         ("seo-dataforseo", "Live SERP and keywords."), ("seo-firecrawl", "Crawl a whole site.")]),
]
assert sum(len(c[2]) for c in COLS) + 1 == 24  # + ai-brand-test = the 24 in the headline

cols = "".join(
    f'<div class=col><div class=head style="background:{fill}">{name}</div>'
    + "".join(f'<div class=tile><b>{html.escape(s)}</b><span>{html.escape(d)}</span></div>' for s, d in skills)
    + "</div>" for name, fill, skills in COLS)

page = f"""<!doctype html><html><head><meta charset=utf-8>
<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&display=block">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;background:#f6f4f0;color:#171614;font-family:'Hanken Grotesk',sans-serif;overflow:hidden}}
.wrap{{padding:64px 56px 0}}
h1{{font-size:104px;font-weight:600;letter-spacing:-0.045em;line-height:.92}}
.sub{{font-size:30px;line-height:1.3;margin-top:22px;max-width:900px;letter-spacing:-0.01em}}
.hero{{margin-top:34px;background:#171614;color:#f6f4f0;padding:26px 30px;display:flex;gap:28px;align-items:center}}
.hero b{{font-size:38px;font-weight:600;letter-spacing:-0.02em;white-space:nowrap}}
.hero span{{font-size:22px;line-height:1.35;color:#d8d4cc}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:22px}}
.col{{display:flex;flex-direction:column;gap:8px}}
.head{{font-size:21px;font-weight:700;padding:14px 14px}}
.tile{{background:#fff;padding:12px 14px;min-height:86px}}
.tile b{{display:block;font-size:18px;font-weight:600;letter-spacing:-0.01em}}
.tile span{{display:block;font-size:16px;line-height:1.3;color:#4a4740;margin-top:5px}}
.cta{{position:absolute;left:56px;right:56px;bottom:110px;background:#ffe14a;padding:28px 32px}}
.cta b{{font-size:50px;font-weight:600;letter-spacing:-0.03em;line-height:1}}
.cta span{{display:block;font-size:24px;margin-top:10px}}
.foot{{position:absolute;left:56px;bottom:46px;font-size:22px}}
.foot i{{font-style:normal;color:#6b675f}}
</style></head><body><div class=wrap>
<h1>AI Visibility Team</h1>
<p class=sub>24 skills for Claude Code that check whether ChatGPT recommends your business, and help you fix it.</p>
<div class=hero><b>ai-brand-test</b><span>Asks your buyers' questions in ChatGPT, Gemini, Google, Claude and Perplexity, then counts who gets named.</span></div>
<div class=grid>{cols}</div>
</div>
<div class=cta><b>Comment “AI” and I’ll send you the pack</b><span>Free. Open source. Installs in 2 minutes.</span></div>
<div class=foot><b>Alex Andronov</b> <i>· AI visibility and automation for businesses</i></div>
</body></html>"""

ICONS = [("openai", "ChatGPT"), ("googlegemini", "Gemini"), ("google", "Google"), ("claude", "Claude"), ("perplexity", "Perplexity")]
LOGOS = " <b>×</b> ".join(f'<span><img src="https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/{i}.svg">{n}</span>' for i, n in ICONS)  # Simple Icons, CC0
FONT = '<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700&display=block">'
banner = f"""<!doctype html><html><head><meta charset=utf-8>{FONT}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:640px;background:#f6f4f0;color:#171614;font-family:'Hanken Grotesk',sans-serif;overflow:hidden}}
.wrap{{padding:84px 80px}}
h1{{font-size:120px;font-weight:600;letter-spacing:-0.045em;line-height:.92}}
p{{font-size:36px;line-height:1.3;margin-top:28px;max-width:1000px;letter-spacing:-0.01em}}
.bar{{position:absolute;left:80px;bottom:72px;background:#ffe14a;padding:18px 26px;font-size:30px;font-weight:600}}
.bar i{{font-style:normal;font-weight:400}}
.logos{{display:flex;align-items:center;gap:22px;margin-top:40px}}
.logos span{{display:flex;align-items:center;gap:12px;font-size:30px;font-weight:600}}.logos img{{width:44px;height:44px}}
.logos b{{font-size:30px;font-weight:400;color:#8a857c}}
</style></head><body><div class=wrap>
<h1>AI Visibility Team</h1>
<p>24 Claude Code skills that check whether AI assistants recommend your business.</p>
<div class=logos>{LOGOS}</div>
</div><div class=bar>Installs in 2 minutes <i>· ai-brand-test, Claude SEO, Humanizer</i></div></body></html>"""


def shot(html_text, name, w, h):
    src = HERE / f"{name}.html"; src.write_text(html_text)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={w},{h}", "--virtual-time-budget=8000",
                    f"--screenshot={HERE / (name + '.png')}", src.as_uri()], check=True, capture_output=True)
    src.unlink()
    print(HERE / (name + ".png"))


shot(page, "poster", 1080, 1350)
shot(banner, "banner", 1280, 640)
