"""Dashboard page — The Hub."""
import reflex as rx
from ..state.base import State
from .ui import corners, glass, hud


def _radar() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-ro1"), rx.box(class_name="ag-ro2"), rx.box(class_name="ag-rhalo"),
        rx.box(
            rx.box(class_name="ag-rring ag-rr1"), rx.box(class_name="ag-rring ag-rr2"),
            rx.box(class_name="ag-rring ag-rr3"), rx.box(class_name="ag-rring ag-rr4"),
            rx.box(class_name="ag-rgrid"),
            rx.box(class_name="ag-rarc ag-ra"), rx.box(class_name="ag-rarc ag-rb"),
            rx.box(class_name="ag-rarc ag-rc"), rx.box(class_name="ag-rarc ag-rd"),
            rx.box(class_name="ag-rsc"), rx.box(class_name="ag-rcen"),
            rx.box(class_name="ag-blip ag-b1"), rx.box(class_name="ag-blip ag-b2"),
            rx.box(class_name="ag-blip ag-b3"), rx.box(class_name="ag-blip ag-b4"),
            rx.text("GPT-4o :: 87%",  class_name="ag-rlbl ag-rl1"),
            rx.text("GROQ :: 91%",    class_name="ag-rlbl ag-rl2"),
            rx.text("LLAMA :: 72%",   class_name="ag-rlbl ag-rl3"),
            rx.text("CLAUDE :: 94%",  class_name="ag-rlbl ag-rl4"),
            rx.text("TRUTH CORE",     class_name="ag-rcore"),
            class_name="ag-drad",
        ),
        class_name="ag-rw",
    )


def _stile(lbl, val, color, ico="◈") -> rx.Component:
    return rx.box(
        corners(),
        rx.box(
            class_name="ag-stile-bg",
            background=f"radial-gradient(ellipse at top left,{color}08,transparent 60%)",
        ),
        rx.vstack(
            rx.hstack(
                rx.text(ico, class_name="ag-stile-ico",
                        style={"color": color, "text_shadow": f"0 0 12px {color}"}),
                hud(lbl),
                spacing="2", align="center",
            ),
            rx.text(
                val,
                class_name="ag-stile-val",
                style={"color": color, "text_shadow": f"0 0 20px {color}, 0 0 40px {color}44"},
            ),
            spacing="2",
        ),
        class_name="ag-stile ag-glass",
        style={
            "background": f"linear-gradient(135deg,{color}08,transparent)",
            "border": f"1px solid {color}25",
        },
    )


def _mrow(s) -> rx.Component:
    sc = rx.cond(s.score >= 70, "#00e5a0", rx.cond(s.score >= 40, "#ffaa00", "#ff0080"))
    name_color = rx.cond(s.is_mock, "rgba(220,185,240,.45)", "#fff")
    score_color = rx.cond(s.is_mock, "rgba(220,185,240,.45)", sc)
    return rx.hstack(
        rx.vstack(
            rx.text(s.name, class_name="ag-mname", style={"color": name_color}),
            rx.cond(
                s.is_mock,
                rx.text(
                    "SIMULATED",
                    font_family="'Orbitron',monospace",
                    font_size="6px", letter_spacing="0.1em",
                    color="rgba(220,185,240,.35)",
                ),
            ),
            spacing="0",
        ),
        rx.box(
            rx.box(
                class_name="ag-bfill",
                width=s.score.to_string() + "%",
                background=rx.cond(s.is_mock, "rgba(220,185,240,.2)", sc),
                height="100%", border_radius="3px",
            ),
            class_name="ag-bwrap",
        ),
        rx.text(
            s.score.to_string(), class_name="ag-mscore",
            style={"color": score_color, "text_shadow": "0 0 10px currentColor",
                   "opacity": rx.cond(s.is_mock, "0.4", "1")},
        ),
        rx.text(s.latency.to_string() + "ms", class_name="ag-mlat"),
        rx.box(class_name="ag-dot", style={
            "background": rx.cond(s.is_mock, "rgba(220,185,240,.25)",
                          rx.cond(s.available, "#00e5a0", "#ff0080")),
            "box_shadow": rx.cond(s.is_mock, "none",
                          rx.cond(s.available, "0 0 8px #00e5a0", "0 0 8px #ff0080")),
        }),
        class_name="ag-mrow", align="center", spacing="3",
    )


def dashboard_page() -> rx.Component:
    return rx.vstack(
        # Header — no duplicate service chips (already in topbar)
        rx.vstack(
            rx.text(
                "THE HUB",
                font_family="'Orbitron',monospace",
                font_size="28px", font_weight="900", letter_spacing="0.06em",
                style={"text_shadow": "0 0 20px rgba(255,0,128,.18)"},
            ),
            rx.text(
                "Air Traffic Control for AI Truth — real-time multi-model monitoring.",
                font_family="'JetBrains Mono',monospace",
                font_size="10px", color="rgba(220,185,240,.45)",
            ),
            spacing="2", align="start", width="100%",
            class_name="ag-dash-header",
        ),

        # Main grid — radar left, stats right
        rx.hstack(
            # Radar panel
            glass(
                corners(),
                rx.vstack(
                    hud("HALLUCINATION RADAR"),
                    rx.center(
                        rx.box(
                            rx.box(class_name="ag-ro1"),
                            rx.box(class_name="ag-ro2"),
                            _radar(),
                            position="relative",
                        ),
                    ),
                    rx.hstack(
                        *[
                            rx.hstack(
                                rx.box(class_name="ag-dot", style={
                                    "background": c, "box_shadow": f"0 0 8px {c}",
                                    "width": "9px", "height": "9px",
                                }),
                                rx.text(l, font_family="'Orbitron',monospace",
                                        font_size="8px", color=c,
                                        style={"text_shadow": f"0 0 6px {c}"}),
                                spacing="2", align="center",
                            )
                            for l, c in [("LOGIC","#ff0080"),("SOURCE","#00cfff"),("TRUTH","#00e5a0")]
                        ],
                        spacing="5", justify="center",
                    ),
                    spacing="4", align="center",
                ),
                class_name="ag-rwrap",
            ),

            # Stats column
            rx.vstack(
                # HUD stat tiles 2×2
                rx.grid(
                    _stile("TRUTH SCORE", State.truth_score, State.score_color, "◎"),
                    _stile("RISK LEVEL",  State.risk_label,  State.score_color, "⚠"),
                    _stile("CONSENSUS",   (State.consensus * 100).to(int).to_string() + "%", "#00cfff", "⎊"),
                    _stile("LATENCY",     State.latency_ms.to_string() + "ms", "#bf5fff", "⟁"),
                    columns="2", spacing="3", width="100%",
                ),

                # Integrity matrix
                glass(
                    corners(),
                    rx.vstack(
                        rx.hstack(
                            hud("INTEGRITY MATRIX"),
                            rx.spacer(),
                            rx.text(
                                State.models.length().to_string() + " models",
                                font_family="'JetBrains Mono',monospace",
                                font_size="10px", color="rgba(220,185,240,.38)",
                            ),
                        ),
                        rx.hstack(
                            rx.text("MODEL", class_name="ag-vcol", width="95px"),
                            rx.spacer(),
                            rx.text("SCORE", class_name="ag-vcol"),
                            rx.text("MS",    class_name="ag-vcol", width="56px", text_align="right"),
                            padding_bottom="8px",
                            border_bottom="1px solid rgba(255,0,128,.1)",
                            width="100%",
                        ),
                        rx.cond(
                            State.models.length() > 0,
                            rx.vstack(
                                rx.foreach(State.models, _mrow),
                                spacing="0", width="100%",
                            ),
                            rx.center(
                                rx.vstack(
                                    rx.text("◎", class_name="ag-empty-i"),
                                    rx.text("Run interrogation to populate", class_name="ag-empty-t"),
                                    align="center", spacing="2",
                                ),
                                padding="28px",
                            ),
                        ),
                        spacing="3", width="100%",
                    ),
                    class_name="ag-pan",
                ),

                spacing="4", flex="1",
            ),

            spacing="4", align="stretch", width="100%",
        ),

        rx.box(
            "⬡  NEW INTERROGATION",
            class_name="ag-btn",
            on_click=State.go_page("interrogate"),
            cursor="pointer",
        ),

        spacing="5", width="100%", class_name="ag-dash",
    )
