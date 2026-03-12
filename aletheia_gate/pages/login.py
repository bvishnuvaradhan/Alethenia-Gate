import asyncio
import reflex as rx


class LoginState(rx.State):
    operator_id: str = ""
    encryption_key: str = ""
    decrypting: bool = False

    def reset_form(self):
        self.operator_id = ""
        self.encryption_key = ""
        self.decrypting = False

    def set_operator_id(self, value: str):
        self.operator_id = value

    def set_encryption_key(self, value: str):
        self.encryption_key = value

    async def handle_login(self):
        if self.decrypting:
            return

        self.decrypting = True
        await asyncio.sleep(2.2)
        self.decrypting = False
        return rx.redirect("/hub")

    async def handle_enter(self, key: str):
        if key == "Enter":
            return await self.handle_login()


def _corner_brackets() -> rx.Component:
    return rx.fragment(
        rx.box(class_name="corner-bracket corner-tl"),
        rx.box(class_name="corner-bracket corner-tr"),
        rx.box(class_name="corner-bracket corner-bl"),
        rx.box(class_name="corner-bracket corner-br"),
    )


def login_page() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-grid-bg"),
        rx.box(
            position="fixed",
            inset="0",
            background="radial-gradient(ellipse at center, transparent 30%, rgba(2,4,10,0.8) 100%)",
            z_index="1",
            pointer_events="none",
        ),
        rx.center(
            rx.box(
                _corner_brackets(),
                rx.cond(~LoginState.decrypting, rx.box(class_name="scan-line")),
                rx.vstack(
                    rx.image(
                        src="/logo.png",
                        alt="Aletheia Gate",
                        class_name="flicker",
                        style={
                            "width": "72px",
                            "height": "72px",
                            "borderRadius": "50%",
                            "objectFit": "cover",
                            "boxShadow": "0 0 30px rgba(255,0,128,0.5), 0 0 60px rgba(0,207,255,0.2)",
                        },
                    ),

                    align="center",
                    spacing="1",
                    margin_bottom="32px",
                ),
                rx.cond(
                    LoginState.decrypting,
                    rx.vstack(
                        rx.text(
                            "DECRYPTING...",
                            style={
                                "fontFamily": "Orbitron, monospace",
                                "fontSize": "14px",
                                "color": "#ff0080",
                                "animation": "pulse 0.6s ease-in-out infinite",
                                "marginBottom": "12px",
                            },
                        ),
                        rx.text(
                            "Verifying operator credentials against secure vault...",
                            style={
                                "fontFamily": "JetBrains Mono, monospace",
                                "fontSize": "10px",
                                "color": "rgba(220,185,240,0.65)",
                                "marginBottom": "4px",
                            },
                        ),
                        rx.text(
                            "Initializing SurrealDB forensic session...",
                            style={
                                "fontFamily": "JetBrains Mono, monospace",
                                "fontSize": "9px",
                                "color": "rgba(220,185,240,0.62)",
                                "marginBottom": "20px",
                            },
                        ),
                        rx.box(
                            rx.box(
                                style={
                                    "height": "100%",
                                    "animation": "dataStream 1s linear infinite",
                                    "backgroundSize": "200% 100%",
                                    "backgroundImage": "linear-gradient(90deg, transparent, #ff0080, #00cfff, transparent)",
                                    "width": "100%",
                                },
                            ),
                            style={
                                "height": "2px",
                                "background": "rgba(255,0,128,0.1)",
                                "borderRadius": "2px",
                                "overflow": "hidden",
                            },
                        ),
                        style={"textAlign": "center", "padding": "40px 0"},
                        spacing="2",
                    ),
                    rx.vstack(
                        rx.vstack(
                            rx.text(
                                "OPERATOR ID",
                                style={
                                    "fontFamily": "Orbitron, monospace",
                                    "fontSize": "8px",
                                    "color": "#00cfff",
                                    "letterSpacing": "0.15em",
                                    "marginBottom": "8px",
                                },
                            ),
                            rx.input(
                                class_name="input-field",
                                type="text",
                                placeholder="Enter callsign...",
                                value=LoginState.operator_id,
                                on_change=LoginState.set_operator_id,
                                on_key_down=LoginState.handle_enter,
                            ),
                            spacing="1",
                            width="100%",
                            margin_bottom="20px",
                        ),
                        rx.vstack(
                            rx.text(
                                "ENCRYPTION KEY",
                                style={
                                    "fontFamily": "Orbitron, monospace",
                                    "fontSize": "8px",
                                    "color": "#00cfff",
                                    "letterSpacing": "0.15em",
                                    "marginBottom": "8px",
                                },
                            ),
                            rx.input(
                                class_name="input-field",
                                type="password",
                                placeholder="Enter encryption key...",
                                value=LoginState.encryption_key,
                                on_change=LoginState.set_encryption_key,
                                on_key_down=LoginState.handle_enter,
                            ),
                            spacing="1",
                            width="100%",
                            margin_bottom="20px",
                        ),
                        rx.button(
                            "◈ INITIATE HANDSHAKE",
                            class_name="btn-primary",
                            on_click=LoginState.handle_login,
                            style={"width": "100%", "textAlign": "center", "marginTop": "8px"},
                        ),
                        spacing="0",
                        width="100%",
                    ),
                ),
                rx.hstack(
                    rx.text(
                        "New operator?",
                        style={"fontFamily": "JetBrains Mono, monospace", "fontSize": "11px", "color": "rgba(220,185,240,0.62)"},
                    ),
                    rx.link(
                        "CREATE CLEARANCE →",
                        href="/signup",
                        style={"fontFamily": "JetBrains Mono, monospace", "fontSize": "11px", "color": "#ff0080"},
                    ),
                    spacing="2",
                    justify="center",
                    margin_top="20px",
                ),
                class_name="glass-pane",
                style={
                    "width": "100%",
                    "maxWidth": "420px",
                    "position": "relative",
                    "zIndex": "2",
                    "padding": "52px",
                    "overflow": "hidden",
                    "boxShadow": "0 0 60px rgba(255,0,128,0.08), 0 0 120px rgba(0,207,255,0.04)",
                },
            ),
            min_height="100vh",
            padding="40px",
        ),
        class_name="ag-root",
        on_mount=LoginState.reset_form,
    )
