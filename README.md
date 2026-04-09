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

## How This Helps in Practice

ALETHEIA GATE helps reduce silent failure in AI-assisted workflows.
Instead of accepting one model output at face value, teams get structured verification signals before acting on information.

Practical benefits:

- Improves trust calibration: operators can distinguish high-confidence outputs from risky ones
- Reduces hallucination risk: claim segments are checked against multi-model and web evidence
- Supports accountability: every interrogation can be stored and revisited in Vault
- Speeds review workflows: highlights uncertainty and flagged segments instead of forcing full manual re-reading
- Enables safer adoption: teams can integrate AI into research and analysis with clearer guardrails

## Who This Is For

- AI product teams that need reliability checks before showing outputs to users
- Research and analyst workflows that require evidence-backed summaries
- Internal knowledge teams that want an auditable AI verification layer
- Developers building human-in-the-loop AI systems

## Example Use Cases

- Validate factual claims in generated reports
- Compare competing model responses and identify contradiction hotspots
- Build confidence scores for operator approval flows
- Maintain an internal verification history for post-incident review

## Core Capabilities

- Multi-model consensus pipeline for stronger verification signals
- Segment-level analysis (verified, uncertain, flagged)
- Web verification and source alignment scoring
- Fact error extraction and correction hints
- User authentication and per-user persistence in MongoDB
- Per-user API key management in Engine Room
- Vault history for previous interrogations and outcomes

## What Makes It Different

- Verification-first design: scoring and evidence are first-class outputs, not afterthoughts
- Segment-level transparency: each part of a response can be marked verified, uncertain, or flagged
- Operator-centric interface: dashboard and vault are built for decision support, not just model demoing
- Pure Python Reflex stack: full-stack development without separate frontend framework complexity

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

## Disclaimer

This system provides evidence-weighted verification signals, not absolute truth.
Use operator judgment for high-impact decisions.
