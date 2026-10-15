<div align="center">

<img src="./assets/readme/hero.svg" width="100%" alt="ShweMind — a personal agent with a browser, terminal, files, and work that keeps going."/>

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![zly168 ready](https://img.shields.io/badge/zly168-relay_ready-005e62)](docs/SETUP.md#configure-the-agent-and-google)
[![multi-user](https://img.shields.io/badge/auth-multi--user-005e62)](docs/FEATURES.md)
[![local-first](https://img.shields.io/badge/mode-local--first-005e62)](docs/RICH-THREADS.md)
[![curated memory](https://img.shields.io/badge/memory-curated-005e62)](docs/MEMORY.md)

**ShweMind is a personal AI agent with its own computer — ask for an outcome, follow the plan, review actions, and come back to the result.**
Built with CopilotKit React Native for iOS, Android, and web.

> Forked from [CopilotKit/OpenMuse](https://github.com/CopilotKit/OpenMuse) (MIT) and rebuilt for real-world use: zly168 relay support, optional Intelligence (local-first mode), real multi-user auth, curated memory, Burmese locale scaffolding.

[What it does](#what-shwemind-does) · [How to use](#how-to-use) · [Why ShweMind](#why-shwemind) · [Docs](docs/README.md)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/mymyanmarland/shwemind)

</div>

> **Alpha, for self-hosting and building on.** See the [roadmap](ROADMAP.md).

## What ShweMind does

Tell it the outcome. It handles the rest — ShweMind runs its **own computer**: a persistent Chromium browser you can watch inline and **take control of** mid-task, a Linux terminal with saved receipts for every command, and workspace files it edits for you. Tasks are durable (pause, resume, retry), goals keep watch while you're away, and the agent maintains its own curated memory across every chat.

<p align="center">
<img src="./assets/readme/terminal.svg" width="760" alt="ShweMind agent session — ask for an outcome, get the work done."/>
</p>

## How to use

**Requirements:** Node 24 LTS, pnpm 11.19.0, and a model key — any OpenAI-compatible endpoint works (e.g. zly168).

```sh
git clone https://github.com/mymyanmarland/shwemind.git shwemind
cd shwemind
pnpm install --frozen-lockfile
cp .env.example .env   # set MODEL, OPENAI_API_KEY, OPENAI_BASE_URL
pnpm dev               # API on :8787
pnpm dev:web           # open localhost:8081
```

Full guide — model config, Google OAuth, browser worker, Render deploy: [docs/SETUP.md](docs/SETUP.md).

## Why ShweMind

- **Watches and takes over a real browser** — persistent Chromium profiles, visible inline in chat, "Take control" anytime.
- **Own Linux computer** — terminal with saved receipts, editable workspace files.
- **Remembers you** — curated memory across every chat, maintained by the agent itself.
- **Multi-user ready** — real signup/login with per-user data isolation, not a shared key.
- **Any model relay** — `OPENAI_BASE_URL` points at zly168 or any OpenAI-compatible endpoint.
- **Local-first** — runs fully without CopilotKit's cloud; the Intelligence key is optional.

<p align="center">
<img src="./assets/readme/features.svg" width="100%" alt="ShweMind highlights: take-control browser, Linux terminal, curated memory, multi-user auth, zly168 relay, local-first mode."/>
</p>

<details>
<summary>How it flows</summary>
<p align="center">
<img src="./assets/readme/architecture.svg" width="100%" alt="ShweMind architecture: apps to API server to agent engine, fanning out to the browser worker and the zly168 model relay."/>
</p>
</details>

## Learn more

- [Setup guide](docs/SETUP.md) — full quick start, deploy, Google OAuth, browser worker
- [Features](docs/FEATURES.md) · [Demos](docs/DEMO.md) · [Architecture](docs/ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md) · [Roadmap](ROADMAP.md)

MIT licensed. Issues and pull requests are welcome.
