---
name: ai-brand-test
description: Test whether ChatGPT, Gemini, Google AI Overviews, Google AI Mode, Claude and Perplexity recommend a business. Use when the user asks "does ChatGPT recommend us?", wants an AI visibility check, or wants to compare their brand with competitors in AI answers.
---

# AI brand test

Ask the questions real buyers ask, to the assistants they ask, and count who gets named. The questions go through the live ChatGPT and Gemini web apps, Google's own AI answers, Claude and Perplexity, so the results are close to what a buyer sees.

## 1. Get the brief

Ask the user, in one message:
- the brand, its category and the country it sells in (two-letter code, e.g. US, GB);
- 2 to 4 competitors.

They need one [treg.to](https://treg.to) key: env var `TREG_API_KEY`, or the file `~/.config/treg/key`. A 20-question test costs about $0.50.

## 2. Write the questions and the brand list

Create a folder `ai-tests/<brand>-<date>/` with two files (see `example/`):

`questions.md`, in exactly this shape:

```
**A. Broad questions**
1. What are the best <category> in <place>?
...
**B. Specific needs**
6. What is the best <category> for <a real buyer situation>?
...
```

Rules: 10 to 20 questions, half broad and half specific. Write them the way a buyer types, never naming the user's brand. Specific needs come from real situations (budget, size, a problem, a use case), because that is where smaller brands win or lose.

`brands.txt`: one brand per line: the user's brand, their competitors, and the other well-known players in the category. Spelling variants go after `|`, e.g. `HubSpot|HubSpot CRM`.

Show both files to the user and let them edit before running.

## 3. Run and summarise

```bash
COUNTRY=US python3 <this skill>/scripts/run_test.py "ai-tests/<folder>"    # add --limit 2 for a 2-question trial
python3 <this skill>/scripts/analyze.py "ai-tests/<folder>" "<Brand>"
```

`run_test.py` saves every answer to `answers.jsonl`. Then skim the answers for brands that are missing from `brands.txt`, add them, and run `analyze.py` again: it reads the saved answers, so re-running is free. `analyze.py` prints and saves `summary.md`.

Some answers come back empty (Google doesn't show an AI Overview or AI Mode answer for every search); the summary counts them separately.

## 4. Report

Tell the user, in plain words:
- share of answers naming them vs each competitor, broad and specific separately;
- how often they are named first;
- the questions where they were never named;
- which assistants name them least;
- the websites the answers cited most: these are the pages that shape the answers.

Then the next step: get onto the cited sites (reviews, lists, comparisons) and make their own pages answer the specific questions. For the on-site work, use the `seo-geo` skill from Claude SEO.

Say how the test was run (assistants, country, date): answers change between runs, so one test is a snapshot.
