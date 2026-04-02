"""Engine Room — 4 panels: AI Models | Web Sources | API Quota | Settings."""
import reflex as rx
from ..state.engine_state import EngineState
from .ui import corners, glass, hud


def _apirow(label: str, placeholder: str, val, on_change, note: str = "") -> rx.Component:
    connected = val != ""
    return rx.vstack(
        rx.hstack(
            hud(label, "ag-h-c"),
            rx.spacer(),
            rx.hstack(
                rx.box(class_name="ag-dot", style={
                    "background":  rx.cond(connected, "#00e5a0", "rgba(255,255,255,.18)"),
                    "box_shadow":  rx.cond(connected, "0 0 8px #00e5a0", "none"),
                }),
                rx.text(
                    rx.cond(connected, "CONNECTED", "DISCONNECTED"),
                    class_name="ag-connlbl",
                    style={"color": rx.cond(connected, "#00e5a0", "rgba(220,185,240,.35)")},
                ),
                spacing="2", align="center",
            ),
            class_name="ag-apih",
        ),
        rx.input(
            placeholder=placeholder, type="password",
            value=val, on_change=on_change,
            class_name="ag-input", width="100%",
        ),
        rx.cond(
            note != "",
            rx.text(note, font_family="'JetBrains Mono',monospace",
                    font_size="9px", color="rgba(220,185,240,.28)"),
        ),
        spacing="1", width="100%", margin_bottom="14px",
    )


def _sysrow(label: str, val, color) -> rx.Component:
    return rx.hstack(
        rx.text(label, class_name="ag-sysn"),
        rx.hstack(
            rx.box(class_name="ag-dot", style={"background": color,
                   "box_shadow": f"0 0 8px {color}", "animation": "pulse 2.5s infinite"}),
            rx.text(val, class_name="ag-sysv", style={"color": color}),
            spacing="2", align="center",
        ),
        class_name="ag-sysrow",
    )


def _quota_row(model: str, quota: str, color: str = "rgba(220,185,240,.5)") -> rx.Component:
    return rx.hstack(
        rx.text(model, font_family="'JetBrains Mono',monospace",
                font_size="10px", color=color, flex="1"),
        rx.text(quota, font_family="'Orbitron',monospace",
                font_size="8px", color="rgba(220,185,240,.4)", letter_spacing="0.1em",
                flex_shrink="0"),
        padding_y="6px",
        border_bottom="1px solid rgba(0,245,255,.05)",
        width="100%", align="center",
    )


def _quota_header(title: str, subtitle: str = "") -> rx.Component:
    return rx.vstack(
        rx.text(title, font_family="'Orbitron',monospace",
                font_size="8px", letter_spacing="0.18em", color="rgba(220,185,240,.55)",
                margin_top="10px"),
        rx.cond(subtitle != "",
            rx.text(subtitle, font_family="'JetBrains Mono',monospace",
                    font_size="9px", color="rgba(220,185,240,.3)"),
        ),
        spacing="0", margin_bottom="2px",
    )


def _toggle(label: str, is_on, key: str) -> rx.Component:
    return rx.hstack(
        rx.text(label, class_name="ag-toglbl"),
        rx.box(
            rx.box(class_name="ag-togknob",
                   left=rx.cond(is_on, "25px", "3px"),
                   background=rx.cond(is_on, "#00cfff", "rgba(255,255,255,.3)"),
                   style={"box_shadow": rx.cond(is_on, "0 0 10px #00cfff", "none")}),
            on_click=EngineState.tog(key),
            class_name="ag-togsw",
            background=rx.cond(is_on, "rgba(0,207,255,.18)", "rgba(255,255,255,.08)"),
            border=rx.cond(is_on, "1px solid #00cfff", "1px solid rgba(255,255,255,.15)"),
        ),
        class_name="ag-tog", width="100%",
    )


def engine_page() -> rx.Component:
    return rx.vstack(
        hud("SYSTEM CONFIGURATION // ENGINE ROOM", "ag-h-p",
            font_size="9px", letter_spacing="0.3em"),
        rx.text("SETTINGS", font_family="'Orbitron',monospace",
                font_size="26px", font_weight="900",
                style={"text_shadow": "0 0 20px rgba(255,0,128,.15)"}),
        rx.text("All free tier. OpenAI optional.",
                font_family="'JetBrains Mono',monospace",
                font_size="10px", color="rgba(220,185,240,.42)"),

        rx.grid(

            # ── Panel 1: Free AI Model Keys ──────────────────────────────────
            glass(corners(), rx.vstack(
                rx.hstack(
                    hud("AI MODEL KEYS"),
                    rx.spacer(),
                    rx.text("ALL FREE", font_family="'Orbitron',monospace",
                            font_size="7px", color="#00e5a0"),
                ),
                _apirow("GROQ — Llama-3.3 (FREE)",
                        "gsk_...", EngineState.groq_key, EngineState.set_groq,
                        "console.groq.com"),
                # Gemini with cascade display
                rx.vstack(
                    rx.hstack(
                        hud("GOOGLE GEMINI (FREE)", "ag-h-c"),
                        rx.spacer(),
                        rx.hstack(
                            rx.box(class_name="ag-dot", style={
                                "background": rx.cond(EngineState.gemini_key!="","#00e5a0","rgba(255,255,255,.18)"),
                                "box_shadow": rx.cond(EngineState.gemini_key!="","0 0 8px #00e5a0","none"),
                            }),
                            rx.text(rx.cond(EngineState.gemini_key!="","CONNECTED","DISCONNECTED"),
                                    class_name="ag-connlbl",
                                    style={"color":rx.cond(EngineState.gemini_key!="","#00e5a0","rgba(220,185,240,.35)")}),
                            spacing="2", align="center",
                        ),
                        class_name="ag-apih",
                    ),
                    rx.input(placeholder="AIza...", type="password",
                             value=EngineState.gemini_key, on_change=EngineState.set_gemini,
                             class_name="ag-input", width="100%"),
                    rx.text("Cascade: 2.5-pro-preview → 2.5-pro → 2.5-flash → 2.5-flash-lite",
                            font_family="'JetBrains Mono',monospace", font_size="9px",
                            color="rgba(0,207,255,.4)"),
                    rx.cond(EngineState.gemini_active_model != "",
                        rx.text("Active: " + EngineState.gemini_active_model,
                                font_family="'JetBrains Mono',monospace", font_size="9px",
                                color="#00e5a0"),
                    ),
                    rx.text("aistudio.google.com/app/apikey",
                            font_family="'JetBrains Mono',monospace", font_size="9px",
                            color="rgba(220,185,240,.28)"),
                    spacing="1", width="100%", margin_bottom="14px",
                ),
                _apirow("COHERE — Command-R (FREE 1K/mo)",
                        "...", EngineState.cohere_key, EngineState.set_cohere,
                        "dashboard.cohere.com"),
                _apirow("ANTHROPIC — Claude-Haiku (OPTIONAL)",
                        "sk-ant-...", EngineState.anthropic_key, EngineState.set_anthropic,
                        "console.anthropic.com"),
                _apirow("OPENAI — GPT-4o-mini (OPTIONAL PAID)",
                        "sk-...", EngineState.openai_key, EngineState.set_openai,
                        "platform.openai.com/api-keys"),
                rx.box("◈  VERIFY ALL CONNECTIONS", class_name="ag-btn",
                       on_click=EngineState.verify, cursor="pointer", margin_top="4px"),
                spacing="0", width="100%",
            ), class_name="ag-pan"),

            # ── Panel 2: Web Source Keys ──────────────────────────────────────
            glass(corners(), rx.vstack(
                hud("WEB VERIFICATION SOURCES"),
                # Always-on
                *[
                    rx.hstack(
                        rx.box(class_name="ag-dot ag-dot-g"),
                        rx.vstack(
                        rx.text(name, font_family="'Orbitron',monospace",
                            font_size="9px", color="#00e5a0"),
                            rx.text(desc, font_family="'JetBrains Mono',monospace",
                                    font_size="9px", color="rgba(220,185,240,.4)"),
                            spacing="0",
                        ),
                        spacing="3", align="center",
                        padding_y="8px",
                        border_bottom="1px solid rgba(0,245,255,.06)",
                        width="100%",
                    )
                    for name, desc in [
                        ("Wikipedia API",   "No key needed — always active"),
                        ("DuckDuckGo",      "pip install ddgs — no key needed"),
                        ("Wikidata SPARQL", "No key needed — structured facts"),
                    ]
                ],
                # System status
                hud("SYSTEM STATUS", margin_top="8px"),
                _sysrow("WIKIPEDIA", "ACTIVE", "#00e5a0"),
                _sysrow("DUCKDUCKGO", "ACTIVE", "#00e5a0"),
                _sysrow("WIKIDATA", "ACTIVE", "#00e5a0"),
                spacing="2", width="100%",
            ), class_name="ag-pan"),

            # ── Panel 3: API QUOTA & USAGE ────────────────────────────────────
            glass(corners(), rx.vstack(
                hud("API QUOTA & USAGE STATUS"),
                rx.text("Limits shown are for free tier.",
                        font_family="'JetBrains Mono',monospace",
                        font_size="9px", color="rgba(220,185,240,.35)",
                        margin_bottom="4px"),

                # Gemini — all 4 models
                _quota_header("GOOGLE GEMINI", "cascade — uses first available"),
                _quota_row("  2.5-pro-preview", "15 req/min · 25/day",    "#00cfff"),
                _quota_row("  2.5-pro",          "2 req/min  · 50/day",    "#00cfff"),
                _quota_row("  2.5-flash",         "10 req/min · 500/day",   "#00cfff"),
                _quota_row("  2.5-flash-lite",    "30 req/min · 1500/day",  "#00cfff"),

                # Groq
                _quota_header("GROQ"),
                _quota_row("  Llama-3.3-70b", "30 req/min · 6000 tok/min", "#00e5a0"),

                # Cohere
                _quota_header("COHERE"),
                _quota_row("  Command-R", "1000 req/month free", "#bf5fff"),

                # Optional paid
                _quota_header("OPTIONAL (PAID)"),
                _quota_row("  Anthropic Claude-Haiku", "Pay-per-token", "rgba(220,185,240,.4)"),
                _quota_row("  OpenAI GPT-4o-mini",     "Pay-per-token", "rgba(220,185,240,.4)"),

                spacing="0", width="100%",
            ), class_name="ag-pan"),

            # ── Panel 4: Radar sensitivity + system status ────────────────────
            glass(corners(), rx.vstack(
                hud("RADAR SENSITIVITY"),
                rx.vstack(
                    rx.hstack(
                        rx.text("Detection Threshold", class_name="ag-slbl"),
                        rx.spacer(),
                        rx.text(EngineState.sensitivity.to_string()+"%",
                                class_name="ag-sval",
                                style={"color":"#00cfff","text_shadow":"0 0 12px rgba(0,207,255,.6)"}),
                        align="center",
                    ),
                    rx.slider(value=[EngineState.sensitivity],
                              on_change=EngineState.set_sens,
                              min=0, max=100, width="100%", color_scheme="pink"),
                    rx.hstack(
                        rx.text("PERMISSIVE", font_family="'JetBrains Mono',monospace",
                                font_size="9px", color="rgba(220,185,240,.32)"),
                        rx.spacer(),
                        rx.text("STRICT", font_family="'JetBrains Mono',monospace",
                                font_size="9px", color="rgba(220,185,240,.32)"),
                    ),
                    spacing="3",
                ),
                hud("ANALYSIS MODULES"),
                _toggle("TEMPORAL CHECK",  EngineState.tog_temporal, "temporal"),
                _toggle("SEMANTIC CHECK",  EngineState.tog_semantic, "semantic"),
                _toggle("FACTUAL CHECK",   EngineState.tog_factual,  "factual"),
                _toggle("REALTIME CHECK",  EngineState.tog_realtime, "realtime"),
                hud("AI MODEL STATUS"),
                _sysrow("GROQ",
                        rx.cond(EngineState.groq_key!="","CONNECTED","NOT SET"),
                        rx.cond(EngineState.groq_key!="","#00e5a0","rgba(220,185,240,.3)")),
                _sysrow("GEMINI",
                        rx.cond(EngineState.gemini_key!="",
                                rx.cond(EngineState.gemini_active_model!="",
                                        EngineState.gemini_active_model,"KEY SET"),
                                "NOT SET"),
                        rx.cond(EngineState.gemini_key!="","#00cfff","rgba(220,185,240,.3)")),
                _sysrow("COHERE",
                        rx.cond(EngineState.cohere_key!="","CONNECTED","NOT SET"),
                        rx.cond(EngineState.cohere_key!="","#bf5fff","rgba(220,185,240,.3)")),
                _sysrow("ANTHROPIC",
                        rx.cond(EngineState.anthropic_key!="","CONNECTED","NOT SET"),
                        rx.cond(EngineState.anthropic_key!="","#00e5a0","rgba(220,185,240,.3)")),
                rx.cond(EngineState.openai_key!="",
                    _sysrow("OPENAI","CONNECTED","#00cfff"),
                ),
                spacing="3", width="100%",
            ), class_name="ag-pan"),

            columns="2", spacing="6", width="100%", class_name="ag-engrid",
        ),

        spacing="4", width="100%", class_name="ag-engpg",
        on_mount=EngineState.load_saved_api_keys,
    )
