# Spidey-Sense

A self-healing GitHub issue radar. It watches "good first issue" listings on
CNCF sandbox repos, keeps a structured copy of that data in this repo, and
repairs its own scraper automatically if the source page's structure changes.

Built for the WeMakeDevs **"Into the Scrape-Verse"** hackathon (Bright Data track).

**Live dashboard:** https://shreya-d2604.github.io/spidey-sense/
**Demo video:** _(added after recording)_

## Why

A "good first issue" radar only helps if it stays accurate, and scrapers
silently break the moment a site's markup shifts. Instead of someone
noticing and fixing it by hand, Spidey-Sense validates every scrape and, if
it looks broken, asks Bright Data's AI to repair the collector and retry —
unattended.

## Targets

- [WasmEdge](https://github.com/WasmEdge/WasmEdge) (Rust/Wasm)
- [bpfman-operator](https://github.com/bpfman/bpfman-operator) (eBPF)

Two targets here as a proof of concept — the same create → run → validate →
heal loop scales to tracking many more projects at once; adding one is just
another collector plus another job in the workflow.

## How Bright Data Scraper Studio is used

Each target is a custom AI-generated collector (`bdata scraper create`), not
a pre-built one — GitHub issue listings aren't in Bright Data's pre-built
scraper library:

| Target | Collector ID |
|---|---|
| WasmEdge | `c_mt35fgejp9fp62uah` |
| bpfman-operator | `c_mt35mnl52ir8v9u3z7` |

The pipeline, per target:
1. `bdata scraper run <collector_id> <url> -o data/<target>.json`
2. `scripts/validate.py` checks the result (valid JSON, non-empty, every
   issue has a title/url/label)
3. If it fails: `bdata scraper heal <collector_id> "<what looked broken>" --auto-approve`,
   then re-run and re-validate. `--auto-approve` is required — heal stops at
   a human approval gate by default, which would hang an unattended CI run.
4. Commit `data/*.json` back to the repo

The demo video shows this with a **manually triggered break** (via `heal`
itself, asked to corrupt the title extraction) — GitHub redesigning its own
page isn't something we can trigger on cue.

## Setup

```bash
git clone https://github.com/shreya-d2604/spidey-sense.git
cd spidey-sense
npm install -g @brightdata/cli@0.3.5
```

Run a scrape locally (needs `BRIGHTDATA_API_KEY` set, or `bdata login -k <key>`):

```bash
bdata scraper run c_mt35fgejp9fp62uah "<target url>" -o data/wasmedge.json
python3 scripts/clean.py data/wasmedge.json
python3 scripts/validate.py data/wasmedge.json
```

The collector IDs above are tied to this project's Bright Data account —
run `scraper create` yourself first to reproduce with your own.

To run in CI: add `BRIGHTDATA_API_KEY` as a repo secret, then Actions →
**Spidey-Sense** → **Run workflow**. No tokens are committed to the repo.

## Example output

From [data/wasmedge.json](data/wasmedge.json):

```json
{
  "title": "[Community] Claim your WasmEdge Swag bag!",
  "url": "https://github.com/WasmEdge/WasmEdge/issues/551",
  "issue_number": "#551",
  "labels": ["good first issue"]
}
```

## AI-assistance disclosure

Claude Code was used for scaffolding, debugging, and drafting the scraper
commands, validation script, and CI workflow. Scraper logic and CI design
were directed, reviewed, and verified end-to-end by the author.

## Maintainer

Built by Shreya for WeMakeDevs' Into the Scrape-Verse hackathon.
