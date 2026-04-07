"""Landing page — pure rx.* components."""
import reflex as rx
from ..state.base import State


def _nav() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.el.img(src="/favicon.ico", alt="Aletheia logo", class_name="ag-logo-ring", style={"border_radius": "50%", "object_fit": "cover"}),
                rx.vstack(rx.text("ALETHEIA", class_name="ag-brand-main"), rx.text("GATE", class_name="ag-brand-sub"), align="start", spacing="0"),
                align="center", spacing="3",
            ),
            rx.hstack(
                rx.link(rx.text("FEATURES",    class_name="ag-nav-link"), href="#capabilities"),
                rx.link(rx.text("HOW IT WORKS", class_name="ag-nav-link"), href="#flow"),
                rx.link(rx.text("MODELS",      class_name="ag-nav-link"), href="#models"),
                rx.link(rx.text("ABOUT",       class_name="ag-nav-link"), href="#pillars"),
                class_name="ag-nav-links",
            ),
            rx.hstack(
                rx.button("LOGIN",      class_name="ag-nav-btn-ghost", on_click=State.go_login),
                rx.button("GET ACCESS", class_name="ag-btn ag-btn-sm", on_click=State.go_signup),
                spacing="3", align="center", flex_shrink="0",
            ),
            justify="between", align="center", class_name="ag-nav-inner", width="100%",
        ),
        class_name="ag-nav", width="100%",
    )


def _radar() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-ro1"), rx.box(class_name="ag-rhalo"),
        rx.box(
            rx.box(class_name="ag-rring ag-rr1"), rx.box(class_name="ag-rring ag-rr2"),
            rx.box(class_name="ag-rring ag-rr3"), rx.box(class_name="ag-rring ag-rr4"), rx.box(class_name="ag-rring ag-rr5"),
            rx.box(class_name="ag-rgrid"),
            rx.box(class_name="ag-rarc ag-ra"), rx.box(class_name="ag-rarc ag-rb"),
            rx.box(class_name="ag-rarc ag-rc"), rx.box(class_name="ag-rarc ag-rd"),
            rx.box(class_name="ag-rsc"), rx.box(class_name="ag-rcen"),
            rx.box(class_name="ag-blip ag-b1"), rx.box(class_name="ag-blip ag-b2"),
            rx.box(class_name="ag-blip ag-b3"), rx.box(class_name="ag-blip ag-b4"),
            rx.text("GPT-4o :: 87%", class_name="ag-rlbl ag-rl1"),
            rx.text("GROQ :: 91%",   class_name="ag-rlbl ag-rl2"),
            rx.text("LLAMA :: 72%",  class_name="ag-rlbl ag-rl3"),
            rx.text("CLAUDE :: 94%", class_name="ag-rlbl ag-rl4"),
            rx.text("TRUTH CORE",    class_name="ag-rcore"),
            class_name="ag-radar",
        ),
        class_name="ag-rw",
    )


def _hero() -> rx.Component:
    stats = [("247,893","TRUTH AUDITS RUN","ag-sv-c"),("94.7%","AVG ACCURACY GAIN","ag-sv-g"),("4","AI MODELS MONITORED","ag-sv-p")]
    return rx.section(
        rx.box(class_name="ag-orb ag-orb-1"), rx.box(class_name="ag-orb ag-orb-2"), rx.box(class_name="ag-orb ag-orb-3"),
        rx.hstack(
            rx.vstack(
                rx.hstack(rx.box(class_name="ag-eline"), rx.text("FORENSIC-GRADE AI AUDITING", class_name="ag-ebrow"), align="center", spacing="3"),
                rx.vstack(rx.text("ALETHEIA", class_name="ag-t1"), rx.text("GATE", class_name="ag-t2"), align="start", spacing="0"),
                rx.vstack(rx.text("VERITAS SINE FINE", class_name="ag-tg1"), rx.text("TRUTH WITHOUT END", class_name="ag-tg2"), align="start", spacing="1", class_name="ag-tgwrap"),
                rx.text("The first forensic-grade Quantum Truth Interface. Built for researchers, developers, and power users who demand verifiable certainty from every AI endpoint.", class_name="ag-copy"),
                rx.hstack(
                    rx.button("⬡ INITIATE QUANTUM HANDSHAKE", class_name="ag-btn", on_click=State.go_signup),
                    rx.button("RETURNING OPERATOR →", class_name="ag-btn-link", on_click=State.go_login),
                    spacing="4", wrap="wrap",
                ),
                rx.hstack(*[rx.vstack(rx.text(v,class_name=f"ag-sv {vc}"),rx.text(l,class_name="ag-sl"),align="start",spacing="1",class_name="ag-si") for v,l,vc in stats], class_name="ag-stats", spacing="0"),
                align="start", spacing="6", class_name="ag-hero-l",
            ),
            rx.box(_radar(), class_name="ag-hero-r"),
            class_name="ag-hero-wrap", align="center", justify="between", spacing="8",
        ),
        class_name="ag-hero",
    )


def _ticker() -> rx.Component:
    t1 = "   ◈ QUERY_ID::7742 → TRUTH_SCORE: 92.4%   ///   ⟁ MODEL::GPT-4o → HALLUCINATION_RISK: LOW   ///   ⎊ GROQ::ACTIVE → LATENCY: 142ms   ///   ◎ INTEGRITY::PASS → VECTOR_MATCH: 0.94   ///   ⬢ AUDIT_LOG::WRITING → BLOCK_7742   ///   ⌬ TEMPORAL_DRIFT::+0.3% → STABLE   ///   "
    t2 = "   SYS::NEURAL_CORE → ONLINE   ///   FORENSIC_ENGINE::v4.2.1 → LOADED   ///   SURREAL_DB::VAULT → CONNECTED   ///   EMBEDDING::text-3-large → ACTIVE   ///   "
    return rx.box(
        rx.box(rx.text(t1, class_name="ag-tki"), class_name="ag-tkrow"),
        rx.box(rx.text(t2, class_name="ag-tki2"), class_name="ag-tkrow2"),
        class_name="ag-tkwrap",
    )


def _step(step,title,desc,icon,color) -> rx.Component:
    return rx.vstack(
        rx.box(icon, class_name="ag-ficon", style={"color":color,"border":f"1px solid {color}66","background":f"{color}18","box_shadow":f"0 0 25px {color}25"}),
        rx.text(f"STEP {step}", class_name="ag-fstep", style={"color":color}),
        rx.text(title, class_name="ag-ftitle"),
        rx.text(desc,  class_name="ag-fdesc"),
        class_name="ag-fi", align="center", spacing="2",
    )


def _flow() -> rx.Component:
    steps=[("01","QUERY INTAKE","Your question is parsed, tokenized and distributed to all connected model endpoints simultaneously.","⟁","#00f5ff"),
           ("02","CROSS-REFERENCE","Each model response is compared against the others and our internal vector truth database.","⎊","#bf5fff"),
           ("03","SCORE & FLAG","A composite Integrity Index score is computed. Divergent claims are flagged as potential hallucinations.","◎","#39ff14"),
           ("04","ARCHIVE & REPORT","The full audit is sealed into the Vault as an immutable cryptographic record.","⬢","#ffaa00")]
    return rx.section(
        rx.vstack(rx.text("— ARCHITECTURAL FLOW —",class_name="ag-kicker ag-col-v"),rx.heading("HOW ALETHEIA WORKS",class_name="ag-stitle ag-holo"),align="center",spacing="2",margin_bottom="2.8rem"),
        rx.box(rx.box(rx.box(class_name="ag-fbeam"),class_name="ag-fline"),rx.hstack(*[_step(*s) for s in steps],class_name="ag-fgrid",align="stretch",spacing="0",wrap="wrap"),position="relative"),
        class_name="ag-sec",
        id="flow",
    )


def _card(title,desc,icon,color) -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-cc ag-cc-tl"),rx.box(class_name="ag-cc ag-cc-tr"),rx.box(class_name="ag-cc ag-cc-bl"),rx.box(class_name="ag-cc ag-cc-br"),
        rx.box(icon,class_name="ag-cicon",style={"color":color,"border":f"1px solid {color}44","background":f"{color}12","box_shadow":f"0 0 18px {color}18"}),
        rx.text(title,class_name="ag-ctitle",style={"color":color,"text_shadow":f"0 0 10px {color}66"}),
        rx.text(desc,class_name="ag-cdesc"),rx.text("EXPLORE →",class_name="ag-cexplore",style={"color":color}),
        class_name="ag-card",style={"--ag-acc":color},
    )


def _caps() -> rx.Component:
    cards=[("HALLUCINATION RADAR","Real-time probabilistic scanning using multi-model cross-referencing with 12-layer neural verification protocols.","◎","#bf5fff"),
           ("INTEGRITY INDEX","Forensic-grade scoring engine assigning confidence ratings to every sentence generated by connected LLM endpoints.","⬡","#00f5ff"),
           ("TRUTH ARCHIVE","Immutable audit trail with cryptographic timestamps — every truth-check preserved in the Vault.","⬢","#39ff14"),
           ("MULTI-MODEL SYNC","Simultaneous interrogation of GPT-4o, Llama, Groq, and Claude. Compare, contrast, and validate in parallel.","⎊","#ffaa00"),
           ("FORENSIC CHAT","Terminal-style interrogation that watches AI reasoning in real-time — word by word, claim by claim.","⟁","#00f5ff"),
           ("DRIFT ANALYTICS","Historical pattern analysis revealing which topics and models drift over time.","⌬","#bf5fff")]
    return rx.section(
        rx.vstack(rx.text("DIAGNOSTIC SUITE",class_name="ag-kicker ag-col-c"),rx.heading("CAPABILITIES",class_name="ag-stitle ag-holo"),align="center",spacing="2",margin_bottom="2.8rem"),
        rx.box(*[_card(*c) for c in cards],class_name="ag-cgrid"),
        class_name="ag-sec",
        id="capabilities",
    )


def _pillar(title,items) -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-pcc ag-pcc-tl"),rx.box(class_name="ag-pcc ag-pcc-tr"),rx.box(class_name="ag-pcc ag-pcc-bl"),rx.box(class_name="ag-pcc ag-pcc-br"),
        rx.text(title,class_name="ag-ptitle",style={"color":"#00cfff"}),
        rx.vstack(*[rx.hstack(rx.box(class_name="ag-pdot",style={"background":"#00cfff","box_shadow":"0 0 6px #00cfff"}),rx.text(i,class_name="ag-pitem"),spacing="2",align="center") for i in items],spacing="2",align="start"),
        class_name="ag-pc",
    )


def _pillars() -> rx.Component:
    return rx.section(
        rx.vstack(rx.text("DESIGNED FOR POWER USERS",class_name="ag-kicker ag-col-p"),rx.heading("BUILT FOR POWER USERS",class_name="ag-stitle ag-holo"),align="center",spacing="2",margin_bottom="2.8rem"),
        rx.box(_pillar("FOR RESEARCHERS",["Forensic audit trails","Multi-model comparison","Integrity scoring","Vault export"]),
               _pillar("FOR DEVELOPERS",["API-first architecture","Realtime streaming","Batch audit mode","Webhook events"]),
               _pillar("FOR COMPLIANCE",["Immutable records","Legal timestamps","Full transparency","GDPR-ready export"]),
               class_name="ag-pgrid"),
        class_name="ag-sec",
        id="pillars",
    )


def _models() -> rx.Component:
    models = [
        ("GPT-4o", "OpenAI", "87%", "#00f5ff", "Advanced reasoning with real-time knowledge integration. State-of-the-art language understanding and code generation."),
        ("CLAUDE", "Anthropic", "94%", "#bf5fff", "Constitutional AI with emphasis on harmful content rejection and nuanced response generation."),
        ("GROQ", "Groq Inc.", "91%", "#39ff14", "High-speed tensor streaming processor optimized for LLM inference and low-latency responses."),
        ("LLAMA", "Meta AI", "72%", "#ffaa00", "Open-source foundation model with efficient fine-tuning capabilities and research flexibility."),
    ]
    return rx.section(
        rx.vstack(
            rx.text("INTEGRATED AI MODELS", class_name="ag-kicker ag-col-c"),
            rx.heading("MULTI-MODEL ARSENAL", class_name="ag-stitle ag-holo"),
            align="center", spacing="2", margin_bottom="2.8rem"
        ),
        rx.box(
            *[
                rx.box(
                    rx.box(class_name="ag-cc ag-cc-tl"), rx.box(class_name="ag-cc ag-cc-tr"),
                    rx.box(class_name="ag-cc ag-cc-bl"), rx.box(class_name="ag-cc ag-cc-br"),
                    rx.vstack(
                        rx.hstack(
                            rx.text(name, font_size="18px", font_weight="700", color=color, text_shadow=f"0 0 12px {color}"),
                            rx.box(class_name="ag-dot ag-dot-a", style={"background": color, "box_shadow": f"0 0 10px {color}"}),
                            align="center", spacing="2",
                        ),
                        rx.text(provider, font_family="'JetBrains Mono',monospace", font_size="11px", color="rgba(220,185,240,.4)"),
                        rx.text(f"ACC: {acc}", font_family="'Orbitron',monospace", font_size="9px", letter_spacing="0.15em", color=color, text_shadow=f"0 0 8px {color}"),
                        rx.text(desc, font_size="11px", color="rgba(220,185,240,.5)", line_height="1.6"),
                        align="start", spacing="2",
                    ),
                    style={"--ag-acc": color},
                    class_name="ag-card",
                )
                for name, provider, acc, color, desc in models
            ],
            class_name="ag-cgrid",
        ),
        class_name="ag-sec",
        id="models",
    )


def _cta() -> rx.Component:
    return rx.section(
        rx.box(class_name="ag-cta-amb"),
        rx.text("— BEGIN YOUR AUDIT —",class_name="ag-kicker ag-col-p"),
        rx.vstack(rx.text("READY TO INTERROGATE",class_name="ag-cta-t1"),rx.text("YOUR AI?",class_name="ag-cta-t2 ag-holo"),spacing="1",align="center"),
        rx.text("Join researchers and developers using Aletheia Gate to verify, audit, and trust the AI outputs that matter.",class_name="ag-cta-copy"),
        rx.hstack(
            rx.button("⬡ CREATE CLEARANCE — FREE",class_name="ag-btn ag-btn-lg",on_click=State.go_signup),
            rx.button("RETURNING OPERATOR",class_name="ag-btn-cta-sec",on_click=State.go_login),
            spacing="4",wrap="wrap",justify="center",
        ),
        class_name="ag-cta",
    )


def _footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(rx.el.img(src="/favicon.ico",alt="Aletheia logo",class_name="ag-logo-ring",style={"width":"36px","height":"36px","border_radius":"50%","object_fit":"cover"}),rx.text("ALETHEIA GATE",class_name="ag-foot-brand"),rx.text("VERITAS SINE FINE",class_name="ag-foot-tag"),spacing="3",align="center"),
            rx.hstack(*[rx.text(l,class_name="ag-foot-link") for l in ["PRIVACY","TERMS","RESEARCH","API"]],spacing="5"),
            rx.hstack(rx.box(class_name="ag-dot ag-dot-g"),rx.text("ALL SYSTEMS NOMINAL",class_name="ag-foot-state"),spacing="2",align="center"),
            class_name="ag-foot-in",justify="between",align="center",
        ),
        class_name="ag-foot",
    )


def landing_page() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-grid-bg"),
        _nav(),
        rx.box(_hero(), _ticker(), _flow(), _caps(), _models(), _pillars(), _cta(), _footer(), class_name="ag-page"),
        class_name="ag-root",
    )
