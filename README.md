# ALETHEIA GATE — Forensic AI Audit Suite

Cyber-noir UI built entirely in **pure Python Reflex** — zero `rx.html()`, zero inline HTML, zero JavaScript files.

---

## Quick Start

```bash
cd aletheia_gate
cp .env.example .env          # optional — runs in mock mode without keys
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
reflex init
reflex run                    # → http://localhost:3000
```

**Requires:** Python 3.11+, Node.js 18+

---

## Architecture

```
aletheia_gate/
├── aletheia_gate.py          ← Single @rx.page entry, top-level router
├── styles.py                 ← ALL CSS — keyframes, components, layouts
│
├── pages/                    ← Frontend — pure rx.* only
│   ├── ui.py                 ← Shared atoms: corners(), glass(), hud(), btn()
│   ├── layout.py             ← sidebar() + topbar() + shell()
│   ├── landing.py            ← Public hero, radar, ticker, features, CTA
│   ├── login.py              ← Login form (rx.input on_change bound to State)
│   ├── signup.py             ← Signup form (rx.input on_change bound to State)
│   ├── dashboard.py          ← HUD stats, pipeline bar, CSS radar, integrity matrix
│   ├── interrogation.py      ← Stream terminal, segment analysis, integrity meter
│   ├── vault.py              ← Audit log table with search
│   ├── engine.py             ← API keys, sliders, module toggles
│   └── terminate.py          ← Session wipe with dramatic animation
│
├── state/                    ← Backend — one file per concern
│   ├── base.py               ← State root: all shared vars + auth + routing
│   ├── interrogation_state.py← IntState: streaming, pipeline, audit
│   ├── vault_state.py        ← VaultState: audit log loading + search
│   ├── engine_state.py       ← EngineState: API keys, sliders, toggles
│   └── terminate_state.py    ← TermState: session wipe sequence
│
└── backend/                  ← Pure Python — no Reflex imports
    ├── truth_engine.py       ← Multi-model consensus pipeline (mock fallback)
    └── vault_db.py           ← In-memory audit store (SurrealDB optional)
```

---

## Why buttons work

Login/signup forms use proper Reflex state bindings:

```python
# State vars
login_user: str = ""
login_pass: str = ""

# Setter events
def set_login_user(self, v: str): self.login_user = v
def set_login_pass(self, v: str): self.login_pass = v

# Submit event (async generator — yields between steps)
async def do_login(self):
    if not self.login_user or not self.login_pass:
        self.err_msg = "Both fields required."; return
    self.status_msg = "Verifying..."
    yield                        # ← UI updates here (shows spinner)
    await asyncio.sleep(1.8)     # ← simulates server auth
    self.authenticated = True
    self.page = "app"
    yield                        # ← UI updates here (shows dashboard)

# In the component
rx.input(
    value=State.login_user,
    on_change=State.set_login_user,  # bound — no JS needed
)
rx.box("INITIATE HANDSHAKE", on_click=State.do_login)
```

---

## Visual effects — all pure CSS via class_name=

| Effect | CSS class |
|---|---|
| Animated grid background | `.ag-grid-bg` |
| Floating ambient orbs | `.ag-orb-1/2/3` |
| Spinning conic gradient logo | `.ag-logo-ring` |
| Holographic glass card | `.ag-glass` (shimmer + holo lines via `::before/::after`) |
| Animated corner brackets | `.ag-c-tl/tr/bl/br` |
| Dual scan line | `.ag-scan` + `.ag-scan2` |
| Pure CSS radar with sweep | `.ag-radar` + `.ag-rsc` + `.ag-rs` |
| Conic gradient arc scores | `.ag-ra/rb/rc/rd` |
| Neon flicker title | `.ag-t1` (animation: nflicker) |
| Holographic gradient text | `.ag-holo` |
| Glowing status dots | `.ag-dot-g/p/c/v` |
| Multi-ring spinner | `.ag-spin` + `.ag-sr1/2/3` |
| Dual ticker tape | `.ag-tki` + `.ag-tki2` |
| Pipeline node ring pulse | `.ag-pdot-a` (animation: nring) |
| Segment reveal | `.ag-seg` (animation: srev) |
| Progress beam | `.ag-bfill::after` (animation: pbeam) |

---

## Adding real API keys

After login, go to **Engine Room** and paste your keys. They are saved to env at runtime:

```
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
```

The truth engine auto-detects keys and uses real models instead of mock responses.
