import asyncio
import reflex as rx


class SignupState(rx.State):
    username: str = ""
    email: str = ""
    password: str = ""
    scanning: bool = False
    active_field: str = ""

    def reset_form(self):
        self.username = ""
        self.email = ""
        self.password = ""
        self.scanning = False
        self.active_field = ""

    def set_username(self, value: str):
        self.username = value

    def set_email(self, value: str):
        self.email = value

    def set_password(self, value: str):
        self.password = value

    def set_active_field(self, field: str):
        self.active_field = field

    async def handle_submit(self):
        if self.scanning:
            return
        self.scanning = True
        await asyncio.sleep(2.0)
        self.scanning = False
        return rx.redirect("/hub")

    async def handle_enter(self, key: str):
        if key == "Enter":
            return await self.handle_submit()


def _corner_brackets() -> rx.Component:
    return rx.fragment(
        rx.box(class_name="corner-bracket corner-tl"),
        rx.box(class_name="corner-bracket corner-tr"),
        rx.box(class_name="corner-bracket corner-bl"),
        rx.box(class_name="corner-bracket corner-br"),
    )


def _input_block(label: str, key_name: str, placeholder: str, input_type: str, value: rx.Var, on_change) -> rx.Component:
    return rx.box(
        rx.text(
            label,
            style={
                "fontFamily": "Orbitron, monospace",
                "fontSize": "8px",
                "color": "rgba(0,207,255,0.75)",
                "letterSpacing": "0.15em",
                "marginBottom": "8px",
            },
        ),
        rx.input(
            class_name="input-field",
            type=input_type,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            on_focus=SignupState.set_active_field(key_name),
            on_blur=SignupState.set_active_field(""),
            on_key_down=SignupState.handle_enter,
            style={
                "borderColor": rx.cond(
                    SignupState.active_field == key_name,
                    "#00cfff",
                    "rgba(0,207,255,0.18)",
                ),
                "borderBottom": rx.cond(
                    SignupState.active_field == key_name,
                    "2px solid #00cfff",
                    "2px solid rgba(0,207,255,0.45)",
                ),
                "boxShadow": rx.cond(
                    SignupState.active_field == key_name,
                    "0 0 18px rgba(0,207,255,0.25), 0 0 6px rgba(0,207,255,0.12)",
                    "none",
                ),
            },
        ),
        rx.cond(
            SignupState.active_field == key_name,
            rx.text(
                "◉ INPUT STREAM ENCRYPTED",
                style={
                    "fontFamily": "JetBrains Mono, monospace",
                    "fontSize": "9px",
                    "color": "#00e5a0",
                    "marginTop": "4px",
                    "letterSpacing": "0.15em",
                },
            ),
        ),
        style={"marginBottom": "24px"},
    )


def signup_page() -> rx.Component:
    return rx.box(
        rx.box(class_name="ag-grid-bg"),
        rx.center(
            rx.box(
                _corner_brackets(),
                rx.box(class_name="scan-line"),
                rx.vstack(
                    rx.text(
                        "CREATE CLEARANCE",
                        style={
                            "fontFamily": "Orbitron, monospace",
                            "fontSize": "22px",
                            "color": "#00cfff",
                            "fontWeight": "700",
                            "marginBottom": "36px",
                        },
                    ),
                    _input_block(
                        "OPERATOR ID",
                        "username",
                        "Enter callsign...",
                        "text",
                        SignupState.username,
                        SignupState.set_username,
                    ),
                    _input_block(
                        "SECURE CHANNEL",
                        "email",
                        "Email endpoint...",
                        "email",
                        SignupState.email,
                        SignupState.set_email,
                    ),
                    _input_block(
                        "ENCRYPTION KEY",
                        "password",
                        "Min 8 chars...",
                        "password",
                        SignupState.password,
                        SignupState.set_password,
                    ),
                    rx.button(
                        rx.cond(
                            SignupState.scanning,
                            rx.hstack(
                                rx.text("◈", style={"display": "inline-block", "animation": "rotate 1s linear infinite"}),
                                rx.text("SCANNING IDENTITY..."),
                                spacing="2",
                                justify="center",
                                align="center",
                            ),
                            rx.text("⬡ INITIALIZE CLEARANCE"),
                        ),
                        class_name="btn-primary",
                        on_click=SignupState.handle_submit,
                        style={"width": "100%", "textAlign": "center", "justifyContent": "center"},
                    ),
                    rx.hstack(
                        rx.text(
                            "Existing operator?",
                            style={"fontFamily": "JetBrains Mono, monospace", "fontSize": "11px", "color": "rgba(220,185,240,0.62)"},
                        ),
                        rx.link(
                            "ACCESS HUB →",
                            href="/login",
                            style={"fontFamily": "JetBrains Mono, monospace", "fontSize": "11px", "color": "#00cfff"},
                        ),
                        spacing="2",
                        justify="center",
                        margin_top="20px",
                    ),
                    width="100%",
                    spacing="0",
                ),
                class_name="glass-pane signup-pane",
                style={
                    "padding": "48px",
                    "position": "relative",
                    "overflow": "hidden",
                    "width": "100%",
                    "maxWidth": "460px",
                },
            ),
            min_height="100vh",
            padding="40px",
        ),
        class_name="ag-root",
        on_mount=SignupState.reset_form,
    )
