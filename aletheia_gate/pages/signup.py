"""Signup page — pure rx.* with proper state bindings."""
import reflex as rx
from ..state.base import State
from .ui import corners, glass


def signup_page() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-grid-bg"),
        rx.box(class_name="ag-orb ag-orb-1"),
        rx.box(class_name="ag-orb ag-orb-2"),
        rx.box(class_name="ag-vign"),

        rx.box(
            rx.box(
                glass(
                    corners(),
                    rx.box(class_name="ag-scan"),
                    rx.box(class_name="ag-scan2"),

                    # Header
                    rx.vstack(
                        rx.text("CREATE CLEARANCE",
                                font_family="'Orbitron',monospace", font_size="22px",
                                font_weight="700", color="#00cfff",
                                style={"text_shadow":"0 0 20px rgba(0,207,255,.4)"}),
                        rx.text("Biometric verification active — session initialized upon clearance.",
                                font_family="'JetBrains Mono',monospace",
                                font_size="11px", color="rgba(220,185,240,.45)",
                                border_left="2px solid rgba(0,207,255,.3)", padding_left="12px"),
                        align="start", spacing="2", margin_bottom="2rem", width="100%",
                    ),

                    # Scanning animation
                    rx.cond(
                        State.status_msg != "",
                        rx.vstack(
                            rx.box(
                                rx.box(class_name="ag-sr ag-sr1", style={"animation": "none"}),
                                rx.box(class_name="ag-sr ag-sr2", style={"animation": "none"}),
                                rx.box(class_name="ag-sr ag-sr3", style={"animation": "none"}),
                                rx.box("◈", class_name="ag-score", style={"animation": "none", "text_shadow": "0 0 10px rgba(255,0,128,.65)", "box_shadow": "0 0 20px rgba(255,0,128,.22) inset"}),
                                class_name="ag-spin", width="80px", height="80px",
                            ),
                            rx.text(State.status_msg, class_name="ag-dtitle"),
                            rx.text("Establishing encrypted operator profile...", class_name="ag-dsub"),
                            rx.text("Generating quantum key pair...",             class_name="ag-dsub2"),
                            rx.box(rx.box(class_name="ag-lfill"), class_name="ag-lbar", width="100%"),
                            rx.hstack(
                                rx.box(class_name="ag-nd ag-nd1"),
                                rx.box(class_name="ag-nd ag-nd2"),
                                rx.box(class_name="ag-nd ag-nd3"),
                                rx.box(class_name="ag-nd ag-nd4"),
                                class_name="ag-nodes",
                            ),
                            align="center", spacing="3", padding_y="2rem",
                        ),
                    ),

                    # Form
                    rx.cond(
                        State.status_msg == "",
                        rx.vstack(
                            rx.vstack(
                                rx.text("OPERATOR ID", class_name="ag-h ag-h-c"),
                                rx.input(
                                    placeholder="Enter callsign...",
                                    value=State.su_user,
                                    on_change=State.set_su_user,
                                    class_name="ag-input",
                                    width="100%",
                                ),
                                align="start", spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("SECURE CHANNEL", class_name="ag-h ag-h-c"),
                                rx.input(
                                    placeholder="Email endpoint...",
                                    type="email",
                                    value=State.su_email,
                                    on_change=State.set_su_email,
                                    class_name="ag-input",
                                    width="100%",
                                ),
                                align="start", spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("ENCRYPTION KEY", class_name="ag-h ag-h-c"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Min 8 chars recommended...",
                                        type=rx.cond(State.show_su_pass, "text", "password"),
                                        value=State.su_pass,
                                        on_change=State.set_su_pass,
                                        class_name="ag-input",
                                        width="100%",
                                    ),
                                    rx.button(
                                        rx.cond(State.show_su_pass, "🙈", "👁"),
                                        on_click=State.toggle_su_pass_visibility,
                                        class_name="ag-nav-btn-ghost",
                                        width="44px",
                                        height="44px",
                                        padding="0",
                                        font_size="18px",
                                    ),
                                    width="100%",
                                    align="center",
                                ),
                                align="start", spacing="1", width="100%",
                            ),
                            rx.cond(
                                State.err_msg != "",
                                rx.text("⚠  " + State.err_msg, class_name="ag-err"),
                            ),
                            rx.box(
                                rx.text("TERMS OF DISCLOSURE", class_name="ag-ttitle"),
                                rx.text(
                                    "All AI outputs are forensic in nature. "
                                    "Scores are probabilistic. Sessions are logged to the Vault.",
                                    class_name="ag-tbody",
                                ),
                                class_name="ag-terms",
                            ),
                            rx.box(
                                "⬡  INITIALIZE CLEARANCE",
                                class_name="ag-btn",
                                on_click=State.do_signup,
                                cursor="pointer",
                                width="100%", text_align="center",
                            ),
                            rx.hstack(
                                rx.text("Existing operator? ", class_name="ag-aswitch"),
                                rx.text("ACCESS HUB →",
                                        class_name="ag-aswitch ag-alink",
                                        on_click=State.go_login, cursor="pointer"),
                                spacing="0",
                            ),
                            rx.text("← BACK TO LANDING",
                                    class_name="ag-back",
                                    on_click=State.go_landing, cursor="pointer",
                                    text_align="center"),
                            align="center", spacing="5", width="100%",
                        ),
                    ),

                    pad="48px",
                ),
                class_name="ag-acard ag-acard-w",
            ),
            class_name="ag-auth",
        ),

        class_name="ag-root", min_height="100vh",
    )
