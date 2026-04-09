# ALETHEIA GATE

Forensic AI audit suite for checking prompt/response credibility with multi-model consensus, web-source verification, and a searchable evidence vault.

## Live App

https://aletheia-gate-teal-panda.reflex.run

## What Is This Project?

ALETHEIA GATE is a full-stack Reflex application designed to audit AI outputs.
It combines multiple model responses, checks claim-level consistency, cross-references web sources, and produces a confidence/risk score with traceable evidence.

## Why This Project Exists

Most LLM outputs look confident even when they are partially wrong.
This project exists to provide an operator-facing verification layer that helps answer:

- Is this response trustworthy?
- Which parts are verified, uncertain, or flagged?
- What external evidence supports or contradicts it?
- Can we keep an audit trail for future review?

## Core Capabilities

- Multi-model consensus pipeline for stronger verification signals
- Segment-level analysis (verified, uncertain, flagged)
- Web verification and source alignment scoring
- Fact error extraction and correction hints
- User authentication and per-user persistence in MongoDB
- Per-user API key management in Engine Room
- Vault history for previous interrogations and outcomes

## How It Works (High Level)

1. User submits a prompt in Interrogation.
2. Truth engine runs multiple models and gathers source evidence.
3. Output is split into segments and scored.
4. Final truth/risk metrics are computed.
5. Results are stored in MongoDB and surfaced in Dashboard, Vault, and Analysis.

## Project Structure

```text
aletheia_gate/
  aletheia_gate.py      # App entry, routes, and app wiring
  styles.py             # Global styles and theme classes
  pages/                # UI pages (landing, login, dashboard, interrogation, etc.)
  state/                # Reflex state classes for auth, engine, vault, analysis, etc.
  backend/              # Truth engine, source verification, and MongoDB persistence
assets/
requirements.txt
rxconfig.py
```

## Tech Stack

- Python 3.11+
- Reflex (frontend + backend)
- MongoDB (users, API keys, query results)
- Optional AI providers: Groq, OpenAI, Gemini, Anthropic, Cohere

## Local Development

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate

pip install -r requirements.txt
reflex run
```

App runs on http://localhost:3000

## Environment Variables

Required in deployment:

- MONGODB_URI

Optional (provider-level fallback keys):

- OPENAI_API_KEY
- GROQ_API_KEY
- GEMINI_API_KEY
- ANTHROPIC_API_KEY
- COHERE_API_KEY
- AG_HF_LOCAL_ONLY (default 1)

Note: In this app flow, provider keys are primarily managed per user and loaded from MongoDB.

## Deployment

Current production deploy target:

- Reflex Cloud

Deployment command:

```bash
reflex deploy --app-id 0b1b547a-4740-4b6f-8e55-a721cae9f3be
```

Secrets are managed with:

```bash
reflex cloud secrets update 0b1b547a-4740-4b6f-8e55-a721cae9f3be --envfile .env --reboot
```

## CI/CD

GitHub Actions auto-deploy is configured on push to main via:

- .github/workflows/reflex-deploy.yml

Required GitHub secret:

- REFLEX_TOKEN

## Disclaimer

This system provides evidence-weighted verification signals, not absolute truth.
Use operator judgment for high-impact decisions.
