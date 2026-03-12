import reflex as rx


def _top_nav() -> rx.Component:
    nav_items = [
        ("FEATURES", "#capabilities"),
        ("HOW IT WORKS", "#how-aletheia-works"),
        ("ABOUT", "#built-for-power-users"),
    ]
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(
                    src="/logo.png",
                    alt="Aletheia Gate",
                    class_name="ag-nav-logo",
                ),
                rx.vstack(
                    rx.text("ALETHEIA", class_name="ag-brand-main"),
                    rx.text("GATE", class_name="ag-brand-sub"),
                    align="start",
                    spacing="0",
                ),
                align="center",
                spacing="3",
            ),
            rx.hstack(
                *[
                    rx.link(
                        rx.text(label, class_name="ag-nav-link"),
                        href=href,
                        text_decoration="none",
                    )
                    for label, href in nav_items
                ],
                class_name="ag-nav-links",
                spacing="1",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "LOGIN",
                        class_name="ag-nav-login",
                    ),
                    href="/login",
                    text_decoration="none",
                ),
                rx.link(
                    rx.button(
                        "GET ACCESS",
                        class_name="ag-btn-primary ag-btn-small",
                    ),
                    href="/signup",
                    text_decoration="none",
                ),
                spacing="3",
                flex_shrink="0",
            ),
            justify="between",
            align="center",
            class_name="ag-nav-inner",
            width="100%",
        ),
        class_name="ag-nav",
        width="100%",
    )


def _hero_stats() -> rx.Component:
    items = [
        ("247,893", "TRUTH AUDITS RUN"),
        ("94.7%", "AVG ACCURACY GAIN"),
        ("4", "AI MODELS MONITORED"),
    ]
    return rx.hstack(
        *[
            rx.vstack(
                rx.text(val, class_name="ag-stat-value"),
                rx.text(label, class_name="ag-stat-label"),
                align="start",
                spacing="1",
                class_name="ag-stat-item",
            )
            for val, label in items
        ],
        class_name="ag-hero-stats",
        spacing="6",
        wrap="wrap",
    )


def _hero() -> rx.Component:
    return rx.section(
        rx.box(class_name="ag-glow ag-glow-left"),
        rx.box(class_name="ag-glow ag-glow-right"),
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.box(class_name="ag-status-dot ag-status-green"),
                    rx.text("QUANTUM TRUTH INTERFACE // ONLINE", class_name="ag-status-text"),
                    align="center",
                    spacing="2",
                ),
                rx.hstack(
                    rx.box(class_name="ag-eyebrow-line"),
                    rx.text("FORENSIC-GRADE AI AUDITING", class_name="ag-eyebrow"),
                    align="center",
                    spacing="3",
                ),
                rx.vstack(
                    rx.text("ALETHEIA", class_name="ag-title-main ag-flicker"),
                    rx.text("GATE", class_name="ag-title-sub"),
                    align="start",
                    spacing="0",
                ),
                rx.vstack(
                    rx.text("VERITAS SINE FINE", class_name="ag-tagline-main"),
                    rx.text("TRUTH WITHOUT END", class_name="ag-tagline-sub"),
                    align="start",
                    spacing="1",
                ),
                rx.text(
                    "The first forensic-grade Quantum Truth Interface. Built for researchers, developers, and power users who demand verifiable certainty - not just answers - from every AI endpoint they touch.",
                    class_name="ag-hero-copy",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            "INITIATE QUANTUM HANDSHAKE",
                            class_name="ag-btn-primary",
                        ),
                        href="/signup",
                        text_decoration="none",
                    ),
                    rx.link(
                        rx.button(
                            "RETURNING OPERATOR ->",
                            class_name="ag-btn-link",
                        ),
                        href="/login",
                        text_decoration="none",
                    ),
                    spacing="4",
                    wrap="wrap",
                ),
                _hero_stats(),
                align="start",
                spacing="6",
                class_name="ag-hero-left",
            ),
            rx.box(
                rx.box(
                    rx.box(class_name="ag-radar-ring ag-radar-ring-1"),
                    rx.box(class_name="ag-radar-ring ag-radar-ring-2"),
                    rx.box(class_name="ag-radar-ring ag-radar-ring-3"),
                    rx.box(class_name="ag-radar-ring ag-radar-ring-4"),
                    rx.box(class_name="ag-radar-grid"),
                    rx.box(class_name="ag-radar-arc ag-radar-arc-a"),
                    rx.box(class_name="ag-radar-arc ag-radar-arc-b"),
                    rx.box(class_name="ag-radar-arc ag-radar-arc-c"),
                    rx.box(class_name="ag-radar-arc ag-radar-arc-d"),
                    rx.box(class_name="ag-radar-sweep-cone"),
                    rx.box(class_name="ag-radar-sweep"),
                    rx.box(class_name="ag-radar-center"),
                    rx.box(class_name="ag-radar-blip ag-radar-blip-1"),
                    rx.box(class_name="ag-radar-blip ag-radar-blip-2"),
                    rx.box(class_name="ag-radar-blip ag-radar-blip-3"),
                    rx.box(class_name="ag-radar-blip ag-radar-blip-4"),
                    rx.text("GPT-4o :: 87%", class_name="ag-radar-label ag-radar-label-1"),
                    rx.text("GROQ :: 91%", class_name="ag-radar-label ag-radar-label-2"),
                    rx.text("LLAMA :: 72%", class_name="ag-radar-label ag-radar-label-3"),
                    rx.text("CLAUDE :: 94%", class_name="ag-radar-label ag-radar-label-4"),
                    rx.text("TRUTH CORE", class_name="ag-radar-core"),
                    class_name="ag-radar",
                ),
                class_name="ag-hero-right",
            ),
            class_name="ag-hero-wrap",
            align="center",
            justify="between",
            spacing="8",
        ),
        class_name="ag-hero",
    )


def _flow_step(step: str, title: str, desc: str, icon: str, color: str) -> rx.Component:
    return rx.vstack(
        rx.box(icon, class_name="ag-flow-icon", style={"color": color, "borderColor": f"{color}66"}),
        rx.text(f"STEP {step}", class_name="ag-flow-step", style={"color": color}),
        rx.text(title, class_name="ag-flow-title"),
        rx.text(desc, class_name="ag-flow-desc"),
        class_name="ag-flow-item",
        align="center",
        spacing="2",
    )


def _how_it_works() -> rx.Component:
    steps = [
        (
            "01",
            "QUERY INTAKE",
            "Your question is parsed, tokenized and routed to all connected model endpoints simultaneously.",
            "△",
            "#00f5ff",
        ),
        (
            "02",
            "CROSS-REFERENCE",
            "Each model response is compared against the others and against our internal vector truth database.",
            "⊘",
            "#bf5fff",
        ),
        (
            "03",
            "SCORE & FLAG",
            "A composite integrity index score is computed. Divergent claims are flagged as potential hallucinations.",
            "◎",
            "#39ff14",
        ),
        (
            "04",
            "ARCHIVE & REPORT",
            "The full audit - query, responses, scores, timestamps - is sealed into the Vault as an immutable record.",
            "⬢",
            "#ffaa00",
        ),
    ]
    return rx.section(
        rx.vstack(
            rx.text("ARCHITECTURAL FLOW", class_name="ag-section-kicker ag-purple"),
            rx.heading("HOW ALETHEIA WORKS", class_name="ag-section-title"),
            align="center",
            spacing="2",
            margin_bottom="2.8rem",
        ),
        rx.hstack(
            *[_flow_step(*s) for s in steps],
            class_name="ag-flow-grid",
            align="stretch",
            spacing="0",
            wrap="wrap",
        ),
        class_name="ag-section",
        id="how-aletheia-works",
    )


def _feature_card(title: str, desc: str, icon: str, color: str) -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-cap-corner ag-cap-corner-tl"),
        rx.box(class_name="ag-cap-corner ag-cap-corner-tr"),
        rx.box(class_name="ag-cap-corner ag-cap-corner-bl"),
        rx.box(class_name="ag-cap-corner ag-cap-corner-br"),
        rx.box(icon, class_name="ag-cap-icon", style={"color": color, "borderColor": f"{color}44", "background": f"{color}12"}),
        rx.text(title, class_name="ag-cap-title", style={"color": color}),
        rx.text(desc, class_name="ag-cap-desc"),
        rx.text("EXPLORE ->", class_name="ag-cap-explore", style={"color": color}),
        class_name="ag-cap-card",
        style={"--ag-cap-accent": color},
    )


def _capabilities() -> rx.Component:
    cards = [
        (
            "HALLUCINATION RADAR",
            "Real-time probabilistic scanning of AI outputs using multi-model cross-referencing with 12-layer neural verification protocols.",
            "◎",
            "#bf5fff",
        ),
        (
            "INTEGRITY INDEX",
            "Forensic-grade scoring engine assigning confidence ratings to every sentence generated by connected LLM endpoints.",
            "⬡",
            "#00f5ff",
        ),
        (
            "TRUTH ARCHIVE",
            "Immutable audit trail with cryptographic timestamps - every truth-check preserved in the Vault for legal accountability.",
            "⬢",
            "#39ff14",
        ),
        (
            "MULTI-MODEL SYNC",
            "Simultaneous interrogation of GPT-4o, Llama, Groq, and Claude endpoints. Compare, contrast, and validate in parallel.",
            "⎊",
            "#ffaa00",
        ),
        (
            "FORENSIC CHAT",
            "Terminal-style interrogation interface that watches the AI's reasoning in real-time - word by word, claim by claim.",
            "⟁",
            "#00f5ff",
        ),
    ]
    return rx.section(
        rx.vstack(
            rx.text("AUDIT CAPABILITIES", class_name="ag-section-kicker ag-cyan"),
            rx.heading("CAPABILITIES", class_name="ag-section-title"),
            align="center",
            spacing="2",
            margin_bottom="2.8rem",
        ),
        rx.vstack(
            *[_feature_card(*c) for c in cards],
            class_name="ag-cap-grid",
            spacing="0",
        ),
        class_name="ag-section",
        id="capabilities",
    )


def _pillar_card(title: str, items: list[str]) -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-pillar-corner ag-pillar-corner-tl"),
        rx.box(class_name="ag-pillar-corner ag-pillar-corner-tr"),
        rx.box(class_name="ag-pillar-corner ag-pillar-corner-bl"),
        rx.box(class_name="ag-pillar-corner ag-pillar-corner-br"),
        rx.text(title, class_name="ag-pillar-title", style={"color": "#00cfff"}),
        rx.vstack(
            *[
                rx.hstack(
                    rx.box(class_name="ag-pillar-dot", style={"background": "#00cfff"}),
                    rx.text(item, class_name="ag-pillar-item"),
                    spacing="2",
                    align="center",
                )
                for item in items
            ],
            spacing="2",
            align="start",
        ),
        class_name="ag-pillar-card",
    )


def _pillars() -> rx.Component:
    return rx.section(
        rx.vstack(
            rx.text("DESIGNED FOR POWER USERS", class_name="ag-section-kicker ag-pink"),
            rx.heading("BUILT FOR POWER USERS", class_name="ag-section-title"),
            align="center",
            spacing="2",
            margin_bottom="2.8rem",
        ),
        rx.vstack(
            *[
                _pillar_card(
                    "FOR RESEARCHERS",
                    [
                        "Forensic audit trails",
                        "Multi-model comparison",
                        "Integrity scoring",
                        "Vault export",
                    ],
                ),
                _pillar_card(
                    "FOR DEVELOPERS",
                    [
                        "API-first architecture",
                        "Realtime streaming",
                        "Batch audit mode",
                        "Webhook events",
                    ],
                ),
                _pillar_card(
                    "FOR COMPLIANCE",
                    [
                        "Immutable records",
                        "Legal timestamps",
                        "Full transparency",
                        "GDPR-ready export",
                    ],
                ),
            ],
            class_name="ag-pillar-grid",
            spacing="2",
        ),
        class_name="ag-section",
        id="built-for-power-users",
    )


def _pillars() -> rx.Component:
    return rx.section(
        rx.vstack(
            rx.text("DESIGNED FOR POWER USERS", class_name="ag-section-kicker ag-pink"),
            rx.heading("BUILT FOR POWER USERS", class_name="ag-section-title"),
            align="center",
            spacing="2",
            margin_bottom="2.8rem",
        ),
        rx.vstack(
            *[
                _pillar_card(
                    "FOR RESEARCHERS",
                    [
                        "Forensic audit trails",
                        "Multi-model comparison",
                        "Integrity scoring",
                        "Vault export",
                    ],
                ),
                _pillar_card(
                    "FOR DEVELOPERS",
                    [
                        "API-first architecture",
                        "Realtime streaming",
                        "Batch audit mode",
                        "Webhook events",
                    ],
                ),
                _pillar_card(
                    "FOR COMPLIANCE",
                    [
                        "Immutable records",
                        "Legal timestamps",
                        "Full transparency",
                        "GDPR-ready export",
                    ],
                ),
            ],
            class_name="ag-pillar-grid",
            spacing="2",
        ),
        class_name="ag-section",
        id="built-for-power-users",
    )


def _cta() -> rx.Component:
    return rx.section(
        rx.box(class_name="ag-cta-ambient"),
        rx.text("- BEGIN YOUR AUDIT -", class_name="ag-section-kicker ag-pink"),
        rx.vstack(
            rx.text("READY TO INTERROGATE", class_name="ag-cta-title-main"),
            rx.text("YOUR AI?", class_name="ag-cta-title-emphasis"),
            class_name="ag-cta-title-wrap",
            spacing="1",
            align="center",
        ),
        rx.text(
            "Join researchers and developers using Aletheia Gate to verify, audit, and trust the AI outputs that matter.",
            class_name="ag-cta-copy",
        ),
        rx.hstack(
            rx.link(
                rx.button(
                    "⬡ CREATE CLEARANCE — FREE",
                    class_name="ag-btn-primary ag-btn-large",
                ),
                href="/signup",
                text_decoration="none",
            ),
            rx.link(
                rx.button(
                    "RETURNING OPERATOR",
                    class_name="ag-nav-login ag-cta-secondary",
                ),
                href="/login",
                text_decoration="none",
            ),
            spacing="4",
            wrap="wrap",
            justify="center",
        ),
        class_name="ag-cta",
    )


def _footer() -> rx.Component:
    links = ["PRIVACY", "TERMS", "RESEARCH", "API"]
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.image(src="/logo.png", alt="Aletheia Gate", class_name="ag-footer-logo"),
                rx.text("ALETHEIA GATE", class_name="ag-footer-brand"),
                rx.text("VERITAS SINE FINE", class_name="ag-footer-tag"),
                spacing="3",
                align="center",
            ),
            rx.hstack(*[rx.text(link, class_name="ag-footer-link") for link in links], spacing="5"),
            rx.hstack(
                rx.box(class_name="ag-status-dot ag-status-green"),
                rx.text("ALL SYSTEMS NOMINAL", class_name="ag-footer-state"),
                spacing="2",
                align="center",
            ),
            class_name="ag-footer-inner",
            justify="between",
            align="center",
        ),
        class_name="ag-footer",
    )


def entry_page() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-grid-bg"),
        _top_nav(),
        rx.box(
            _hero(),
            _how_it_works(),
            _capabilities(),
            _pillars(),
            _cta(),
            _footer(),
            class_name="ag-page",
        ),
        class_name="ag-root",
    )
