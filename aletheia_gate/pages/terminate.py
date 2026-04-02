"""Terminate session page."""
import reflex as rx
from ..state.base import State
from ..state.terminate_state import TermState
from .ui import glass

def terminate_page():
    return rx.center(
        glass(
            rx.vstack(
                # Pulsing icon with rings
                rx.box(
                    rx.box(class_name="ag-tr1"),
                    rx.box(class_name="ag-tr2"),
                    rx.text("⬡", class_name="ag-tico"),
                    position="relative", width="72px", height="72px",
                    display="flex", align_items="center", justify_content="center",
                ),
                rx.text("TERMINATE SESSION", class_name="ag-ttl"),
                rx.box(class_name="ag-tdiv"),
                rx.text(
                    "This will purge all session data, audit logs, and API keys from memory.\n"
                    "The quantum connection will be severed permanently.",
                    class_name="ag-tcopy",
                ),
                # Warning chips
                rx.hstack(
                    *[
                        rx.vstack(
                            rx.text(ico, class_name="ag-twico", style={"color": c, "text_shadow": f"0 0 10px {c}"}),
                            rx.text(msg, class_name="ag-twmsg", style={"color": c}),
                            align="center", spacing="2",
                            padding="14px 18px", border_radius="4px",
                            style={"border": f"1px solid {c}25", "background": f"{c}06"},
                        )
                        for ico, msg, c in [("◉","SESSION DATA","#ff0080"),("⬢","VAULT RECORDS","#ffaa00"),("⚙","API KEYS","#00cfff")]
                    ],
                    spacing="3",
                ),
                # Terminating state
                rx.cond(
                    TermState.terminating,
                    rx.vstack(
                        rx.box(
                            rx.box(class_name="ag-sr ag-sr1"),
                            rx.box(class_name="ag-sr ag-sr2"),
                            rx.box(class_name="ag-sr ag-sr3"),
                            class_name="ag-spin", width="50px", height="50px",
                        ),
                        rx.hstack(
                            rx.box(class_name="ag-nd ag-nd1"),
                            rx.box(class_name="ag-nd ag-nd2"),
                            rx.box(class_name="ag-nd ag-nd3"),
                            rx.box(class_name="ag-nd ag-nd4"),
                            class_name="ag-nodes",
                        ),
                        rx.text(State.status_msg, class_name="ag-tstat"),
                        rx.box(rx.box(class_name="ag-lfill"), class_name="ag-lbar", width="340px"),
                        align="center", spacing="3",
                    ),
                    # Confirm / abort buttons
                    rx.hstack(
                        rx.box(
                            "◉  CONFIRM TERMINATE",
                            class_name="ag-btn",
                            on_click=TermState.terminate,
                            cursor="pointer",
                        ),
                        rx.box(
                            "← ABORT",
                            on_click=State.go_page("dashboard"),
                            cursor="pointer",
                            font_family="'Orbitron',monospace",
                            font_size="11px", letter_spacing="0.2em",
                            color="rgba(220,185,240,.5)",
                            padding="13px 32px",
                            border="1px solid rgba(0,207,255,.25)", border_radius="2px",
                            style={"transition": "all .25s", "_hover": {"color": "#00cfff", "border_color": "#00cfff", "box_shadow": "0 0 15px rgba(0,207,255,.2)"}},
                        ),
                        spacing="4",
                    ),
                ),
                align="center", spacing="5",
            ),
            class_name="ag-tpg",
        ),
        class_name="ag-twrap",
    )
