"""Login page — pure rx.* with proper state bindings."""
import reflex as rx
from ..state.base import State
from .ui import corners, glass


def login_page() -> rx.Component:
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

                    # Spinning logo
                    rx.vstack(
                        rx.el.img(
                            src="/favicon.ico",
                            alt="Aletheia logo",
                            class_name="ag-alogo",
                            style={"border_radius": "50%", "object_fit": "cover"},
                        ),
                        rx.text("SESSION INITIALIZATION PROTOCOL", class_name="ag-h"),
                        align="center", spacing="1", margin_bottom="2rem",
                    ),

                    # Decrypting animation
                    rx.cond(
                        State.status_msg != "",
                        rx.vstack(
                            rx.box(
                                rx.box(class_name="ag-sr ag-sr1"),
                                rx.box(class_name="ag-sr ag-sr2"),
                                rx.box(class_name="ag-sr ag-sr3"),
                                rx.box("◈", class_name="ag-score"),
                                class_name="ag-spin", width="60px", height="60px",
                            ),
                            rx.text(State.status_msg, class_name="ag-dtitle"),
                            rx.text("Verifying credentials against vault...", class_name="ag-dsub"),
                            rx.text("Initializing forensic session...",       class_name="ag-dsub2"),
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

                    # Form (hidden during loading)
                    rx.cond(
                        State.status_msg == "",
                        rx.vstack(
                            rx.vstack(
                                rx.text("OPERATOR ID", class_name="ag-h ag-h-c"),
                                rx.input(
                                    placeholder="Enter callsign...",
                                    value=State.login_user,
                                    on_change=State.set_login_user,
                                    class_name="ag-input",
                                    width="100%",
                                ),
                                align="start", spacing="1", width="100%",
                            ),
                            rx.vstack(
                                rx.text("ENCRYPTION KEY", class_name="ag-h ag-h-c"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Enter encryption key...",
                                        type=rx.cond(State.show_login_pass, "text", "password"),
                                        value=State.login_pass,
                                        on_change=State.set_login_pass,
                                        class_name="ag-input",
                                        width="100%",
                                    ),
                                    rx.button(
                                        rx.cond(State.show_login_pass, "🙈", "👁"),
                                        on_click=State.toggle_login_pass_visibility,
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
                                "◈  INITIATE HANDSHAKE",
                                class_name="ag-btn",
                                on_click=State.do_login,
                                cursor="pointer",
                                width="100%", text_align="center",
                            ),
                            rx.hstack(
                                rx.text("New operator? ", class_name="ag-aswitch"),
                                rx.text("CREATE CLEARANCE →",
                                        class_name="ag-aswitch ag-alink",
                                        on_click=State.go_signup, cursor="pointer"),
                                spacing="0",
                            ),
                            rx.text("← BACK TO LANDING",
                                    class_name="ag-back",
                                    on_click=State.go_landing, cursor="pointer",
                                    text_align="center"),
                            align="center", spacing="5", width="100%",
                        ),
                    ),

                    pad="52px",
                ),
                class_name="ag-acard",
            ),
            class_name="ag-auth",
        ),

        class_name="ag-root", min_height="100vh",
    )
