# Spidey-Sense

Self-healing GitHub issue radar for CNCF sandbox projects. Watches "good
first issue" labels, validates every scrape, and asks Bright Data's AI to
repair its own collector if a page's structure changes — no human needed.

Built for WeMakeDevs' **Into the Scrape-Verse** hackathon (Bright Data track).

**Live dashboard:** https://shreya-d2604.github.io/spidey-sense/


## Targets

- [WasmEdge](https://github.com/WasmEdge/WasmEdge) (Rust/Wasm) — collector `c_mt35fgejp9fp62uah`
- [bpfman-operator](https://github.com/bpfman/bpfman-operator) (eBPF) — collector `c_mt35mnl52ir8v9u3z7`

Two here as a proof of concept — the same loop scales to tracking many more.

## How It Works

1. `bdata scraper run <collector_id> <url> -o data/<target>.json`
2. `scripts/validate.py` checks the result is real, non-empty, and complete
3. If it fails: `bdata scraper heal <collector_id> "<what broke>" --auto-approve`,
   then re-run and re-validate (`--auto-approve` skips heal's human approval
   gate, which would otherwise hang CI)
4. Commit `data/*.json` back to the repo

Each collector is custom-built with `bdata scraper create` — GitHub issue
listings aren't in Bright Data's pre-built scraper library.

## Setup

```bash
git clone https://github.com/shreya-d2604/spidey-sense.git
npm install -g @brightdata/cli@0.3.5
bdata scraper run c_mt35fgejp9fp62uah "<target url>" -o data/wasmedge.json
python3 scripts/clean.py data/wasmedge.json && python3 scripts/validate.py data/wasmedge.json
```

To run in CI: add `BRIGHTDATA_API_KEY` as a repo secret, then Actions →
**Spidey-Sense** → **Run workflow**.

## AI Assistance

Claude was used to help build this project.

## Maintainer

Built by Shreya for WeMakeDevs' Into the Scrape-Verse hackathon.
