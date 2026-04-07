"""App shell — sidebar + topbar. Full width, no dead space."""
import reflex as rx
from ..state.base import State
from ..state.vault_state import VaultState
from ..state.interrogation_state import IntState

NAV = [
    ("hub",         "◈", "The Hub"),
    ("interrogate", "⟁", "Interrogation"),
    ("vault",       "⬢", "The Vault"),
    ("engine",      "⚙", "Engine Room"),
]


def _ni(pid: str, ico: str, lbl: str) -> rx.Component:
    active = State.active_page == pid
    return rx.hstack(
        rx.text(
            ico,
            class_name="ag-niico",
            style={
                "color": rx.cond(active, "#ff0080", "rgba(220,185,240,.42)"),
                "text_shadow": rx.cond(active, "0 0 14px rgba(255,0,128,.9)", "none"),
            },
        ),
        rx.text(
            lbl,
            style={"color": rx.cond(active, "#ff0080", "rgba(220,185,240,.42)")},
        ),
        # Use appropriate handler for each page
        on_click=(State.go_hub_with_load if pid == "hub"
                  else VaultState.go_vault if pid == "vault"
                  else IntState.go_interrogate if pid == "interrogate"
                  else State.go_page(pid)),
        class_name=rx.cond(active, "ag-ni ag-ni-a", "ag-ni"),
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        # Logo
        rx.hstack(
            rx.el.img(src="/favicon.ico", alt="Aletheia logo", class_name="ag-logo-ring", style={"border_radius": "50%", "object_fit": "cover"}),
            rx.vstack(
                rx.text("ALETHEIA",       class_name="ag-brand-main"),
                   rx.text("GATE", class_name="ag-brand-sub"),
                align="start", spacing="0",
            ),
            align="center", spacing="3",
            class_name="ag-sbl",
        ),
        # Status
        rx.hstack(
            rx.box(class_name="ag-dot ag-dot-g"),
            rx.text(
                "CORE: OPTIMAL",
                font_family="'Orbitron',monospace",
                font_size="8px", color="#00e5a0", letter_spacing="0.12em",
            ),
            spacing="2", align="center",
            class_name="ag-sbst",
        ),
        # Nav items
        rx.box(
            *[_ni(*n) for n in NAV],
            flex="1", padding_y="10px",
        ),
        # Truth score (always visible; reflects dashboard aggregate when loaded)
        rx.vstack(
            rx.text("TRUTH SCORE", class_name="ag-scorelbl"),
            rx.text(
                State.truth_score,
                class_name="ag-scorenum",
                style={
                    "color": State.score_color,
                    "text_shadow": "0 0 25px currentColor, 0 0 50px currentColor",
                },
            ),
            rx.text(
                State.risk_label,
                font_family="'Orbitron',monospace",
                font_size="8px", letter_spacing="0.12em",
                style={"color": State.score_color, "text_shadow": "0 0 10px currentColor"},
            ),
            align="center", spacing="1",
            class_name="ag-sbscore",
        ),
        # Operator
        rx.vstack(
            rx.text("OPERATOR", class_name="ag-oplbl"),
            rx.text(State.username, class_name="ag-opname"),
            spacing="1", class_name="ag-sbop",
        ),
        # Terminate
        rx.box(
            rx.box(
                "◉  TERMINATE SESSION",
                class_name="ag-termbtn",
                on_click=State.logout,
                cursor="pointer", width="100%",
            ),
            padding="14px",
            border_top="1px solid rgba(255,0,128,.12)",
        ),
        class_name="ag-sb",
    )


def topbar() -> rx.Component:
    svc_always = []
    return rx.hstack(
        rx.hstack(
            rx.box(class_name="ag-tbbar"),
            rx.text(State.active_page.upper(), class_name="ag-tbpage"),
            spacing="3", align="center",
        ),
        rx.spacer(),
        rx.cond(
            State.status_msg != "",
            rx.hstack(
                rx.box(class_name="ag-dot ag-dot-c"),
                rx.text(State.status_msg, class_name="ag-tbmsgt"),
                spacing="2", align="center",
                class_name="ag-tbmsg",
            ),
        ),
        rx.hstack(
            *[
                rx.hstack(
                    rx.box(class_name="ag-dot", style={"background": c, "box_shadow": f"0 0 8px {c}"}),
                    rx.text(l, font_family="'Orbitron',monospace", font_size="7px", color=c,
                            letter_spacing="0.1em", style={"text_shadow": f"0 0 6px {c}"}),
                    spacing="2", align="center", padding="5px 10px",
                    background=f"{c}06", border=f"1px solid {c}22",
                    border_radius="3px", class_name="ag-svc",
                )
                for l, c in svc_always
            ],
            # OpenAI chip — only shown when key is set
            rx.cond(
                State.openai_active,
                rx.hstack(
                    rx.box(class_name="ag-dot", style={"background": "#00cfff", "box_shadow": "0 0 8px #00cfff"}),
                    rx.text("OPENAI", font_family="'Orbitron',monospace", font_size="7px",
                            color="#00cfff", letter_spacing="0.1em",
                            style={"text_shadow": "0 0 6px #00cfff"}),
                    spacing="2", align="center", padding="5px 10px",
                    background="#00cfff06", border="1px solid #00cfff22",
                    border_radius="3px", class_name="ag-svc",
                ),
            ),
            spacing="2",
        ),
        class_name="ag-tb",
        width="100%",
    )


def shell(content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            topbar(),
            rx.box(
                content,
                flex="1",
                padding="32px 40px",
                overflow_y="auto",
                width="100%",
            ),
            height="100vh",
            overflow="hidden",
            flex="1",
            spacing="0",
            background="#03050d",
            min_width="0",  # prevents flex children from overflowing
        ),
        align="stretch",
        spacing="0",
        min_height="100vh",
        width="100%",
    )
