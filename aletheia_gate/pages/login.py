import reflex as rx
import re

PRIMARY_CYAN = "#00E5FF"
DARK_BG = "#0B0F1A"
VERIFIED_GREEN = "#00FF9C"
ERROR_RED = "#FF4D6D"


class LoginState(rx.State):
    email: str = ""
    password: str = ""
    email_error: str = ""
    password_error: str = ""
    general_error: str = ""

    def reset_form(self):
        """Clear form on page load so previous inputs don't persist."""
        self.email = ""
        self.password = ""
        self.email_error = ""
        self.password_error = ""
        self.general_error = ""

    def set_email(self, value: str):
        self.email = value
        if self.email_error:
            self.email_error = ""

    def set_password(self, value: str):
        self.password = value
        if self.password_error:
            self.password_error = ""

    def validate(self) -> bool:
        valid = True
        if not self.email:
            self.email_error = "Email is required."
            valid = False
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.email_error = "Enter a valid email address."
            valid = False
        if not self.password:
            self.password_error = "Password is required."
            valid = False
        elif len(self.password) < 6:
            self.password_error = "Password must be at least 6 characters."
            valid = False
        return valid

    def handle_login(self):
        self.general_error = ""
        if self.validate():
            # Placeholder: in real app, verify credentials here
            # On success → redirect to hub
            return rx.redirect("/hub")
        else:
            self.general_error = "Please fix the errors above."

    def handle_enter(self, key: str):
        """Submit on Enter key press."""
        if key == "Enter":
            return self.handle_login()


def _glitch_heading(text: str, is_gradient: bool = False) -> rx.Component:
    cls = "glitch-wrapper gradient-text-cyan" if is_gradient else "glitch-wrapper"
    color = "transparent" if is_gradient else "white"
    return rx.html(
        f'<div class="{cls}" data-text="{text}" style="font-size:3rem;font-weight:900;font-family:Orbitron,sans-serif;letter-spacing:4px;color:{color};line-height:1;">{text}</div>'
    )


def _data_lines() -> rx.Component:
    lines = [
        ("01101000", "5%", "1s", "2"),
        ("VERIFIED", "30%", "2.5s", "2.5"),
        ("ACCESS::OK", "55%", "0.5s", "3"),
        ("01010101", "75%", "1.8s", "2"),
        ("NEURAL//NET", "90%", "0.2s", "3.5"),
    ]
    return rx.box(
        *[
            rx.html(
                f'<div class="data-stream-line" style="left:{l};animation-delay:{d}s;animation-duration:{dur}s;">{t}</div>'
            )
            for t, l, d, dur in lines
        ],
        position="absolute",
        inset="0",
        overflow="hidden",
        pointer_events="none",
    )


def _error_msg(msg: rx.Var) -> rx.Component:
    return rx.cond(
        msg != "",
        rx.hstack(
            rx.icon(tag="circle-alert", size=12, color=ERROR_RED),
            rx.text(msg, size="1", color=ERROR_RED, font_family="Exo 2, sans-serif"),
            spacing="1",
            align="center",
            margin_top="0.3em",
        ),
    )


def login_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="fixed", inset="0",
            background=DARK_BG, class_name="neural-grid", z_index="-3",
        ),
        rx.box(
            position="fixed", top="-10%", left="-10%",
            width="600px", height="600px",
            background="radial-gradient(circle, rgba(0,229,255,0.10) 0%, transparent 70%)",
            border_radius="50%", filter="blur(100px)", z_index="-2",
            class_name="animate-pulse",
        ),
        rx.box(
            position="fixed", bottom="-10%", right="-10%",
            width="500px", height="500px",
            background="radial-gradient(circle, rgba(196,76,255,0.08) 0%, transparent 70%)",
            border_radius="50%", filter="blur(100px)", z_index="-2",
        ),

        rx.center(
            rx.box(
                rx.hstack(
                    # === LEFT PANEL ===
                    rx.box(
                        rx.box(class_name="noise-bg"),
                        rx.box(class_name="scanline"),
                        _data_lines(),
                        _glitch_heading("WELCOME"),
                        _glitch_heading("BACK", is_gradient=True),

                        rx.hstack(
                            rx.box(width="8px", height="8px", background=VERIFIED_GREEN,
                                   border_radius="50%", class_name="verified-pulse fast-glow"),
                            rx.text("SYSTEM ONLINE", size="1", color=VERIFIED_GREEN, weight="bold",
                                    letter_spacing="2px", font_family="JetBrains Mono, monospace"),
                            align="center", spacing="2", margin_top="1.5em",
                        ),
                        rx.text(
                            "Access the portal to truth. Your digital identity is being verified.",
                            size="2", color="#64748B", text_align="center",
                            line_height="1.8", font_family="Exo 2, sans-serif",
                            margin_top="1.5em", margin_x="1em",
                        ),
                        rx.html('<div style="width:60%;height:1px;background:linear-gradient(to right,transparent,rgba(0,229,255,0.4),transparent);margin:1.5em auto;"></div>'),
                        rx.hstack(
                            rx.vstack(
                                rx.text("99.9%", size="4", color=PRIMARY_CYAN, weight="bold", font_family="Orbitron, sans-serif"),
                                rx.text("Uptime", size="1", color="#475569", font_family="Exo 2, sans-serif"),
                                align="center", spacing="0",
                            ),
                            rx.html('<div style="width:1px;height:40px;background:rgba(255,255,255,0.08);"></div>'),
                            rx.vstack(
                                rx.text("256b", size="4", color=PRIMARY_CYAN, weight="bold", font_family="Orbitron, sans-serif"),
                                rx.text("Encrypted", size="1", color="#475569", font_family="Exo 2, sans-serif"),
                                align="center", spacing="0",
                            ),
                            rx.html('<div style="width:1px;height:40px;background:rgba(255,255,255,0.08);"></div>'),
                            rx.vstack(
                                rx.text("∞", size="4", color=PRIMARY_CYAN, weight="bold", font_family="Orbitron, sans-serif"),
                                rx.text("Access", size="1", color="#475569", font_family="Exo 2, sans-serif"),
                                align="center", spacing="0",
                            ),
                            justify="center", spacing="5", margin_top="1em",
                        ),

                        display="flex", flex_direction="column",
                        align_items="center", justify_content="center",
                        width="42%", background="rgba(0,0,0,0.45)",
                        position="relative", overflow="hidden", padding="4em 2em",
                    ),

                    # === RIGHT PANEL: FORM ===
                    rx.vstack(
                        rx.vstack(
                            rx.html('<div style="font-size:1.4rem;font-weight:900;font-family:Orbitron,sans-serif;letter-spacing:2px;color:white;">Login</div>'),
                            rx.text("Secure access to your neural environment", size="1", color="#64acca", font_family="Exo 2, sans-serif"),
                            align="center", spacing="1", margin_bottom="2em",
                        ),

                        # General error banner
                        rx.cond(
                            LoginState.general_error != "",
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="triangle-alert", size=14, color=ERROR_RED),
                                    rx.text(LoginState.general_error, size="1", color=ERROR_RED, weight="bold"),
                                    spacing="2", align="center",
                                ),
                                width="100%", padding="0.8em 1.2em",
                                background="rgba(255,77,109,0.08)",
                                border="1px solid rgba(255,77,109,0.3)",
                                border_radius="10px",
                                margin_bottom="0.5em",
                            ),
                        ),

                        # Inputs
                        rx.vstack(
                            # Email field
                            rx.vstack(
                                rx.text("EMAIL", size="1", color=PRIMARY_CYAN, weight="bold", letter_spacing="2px", font_family="Orbitron, sans-serif"),
                                rx.input(
                                    placeholder="Enter your email",
                                    type="email",
                                    value=LoginState.email,
                                    on_change=LoginState.set_email,
                                    width="100%", height="3.2em",
                                    background="rgba(8, 14, 30, 0.8)",
                                    border=rx.cond(
                                        LoginState.email_error != "",
                                        f"1px solid {ERROR_RED}",
                                        "1px solid rgba(0, 229, 255, 0.15)",
                                    ),
                                    color="white",
                                    padding_x="1.5em", border_radius="12px",
                                    font_family="JetBrains Mono, monospace",
                                    font_size="0.9em",
                                    _focus={
                                        "border_color": PRIMARY_CYAN,
                                        "box_shadow": "0 0 25px rgba(0, 229, 255, 0.25)",
                                        "background": "rgba(0, 229, 255, 0.04)",
                                    },
                                    on_key_down=LoginState.handle_enter,
                                ),
                                _error_msg(LoginState.email_error),
                                spacing="1", width="100%",
                            ),

                            # Password field
                            rx.vstack(
                                rx.text("PASSWORD", size="1", color=PRIMARY_CYAN, weight="bold", letter_spacing="2px", font_family="Orbitron, sans-serif"),
                                rx.input(
                                    placeholder="Enter your password",
                                    type="password",
                                    value=LoginState.password,
                                    on_change=LoginState.set_password,
                                    width="100%", height="3.2em",
                                    background="rgba(8, 14, 30, 0.8)",
                                    border=rx.cond(
                                        LoginState.password_error != "",
                                        f"1px solid {ERROR_RED}",
                                        "1px solid rgba(0, 229, 255, 0.15)",
                                    ),
                                    color="white",
                                    padding_x="1.5em", border_radius="12px",
                                    font_family="JetBrains Mono, monospace",
                                    font_size="0.9em",
                                    _focus={
                                        "border_color": PRIMARY_CYAN,
                                        "box_shadow": "0 0 25px rgba(0, 229, 255, 0.25)",
                                        "background": "rgba(0, 229, 255, 0.04)",
                                    },
                                    on_key_down=LoginState.handle_enter,
                                ),
                                _error_msg(LoginState.password_error),
                                spacing="1", width="100%",
                            ),

                            spacing="4", width="100%",
                        ),

                        # Login button
                        rx.button(
                            "Login",
                            on_click=LoginState.handle_login,
                            width="100%", height="3.4em",
                            background=f"linear-gradient(135deg, {PRIMARY_CYAN}, #0095ff)",
                            color="#000d1a", border="none", border_radius="12px",
                            font_family="Orbitron, sans-serif", font_weight="900",
                            letter_spacing="3px", font_size="0.85rem",
                            cursor="pointer", margin_top="2em",
                            box_shadow="0 0 20px rgba(0,229,255,0.3), 0 4px 15px rgba(0,0,0,0.4)",
                            transition="all 0.4s ease",
                            _hover={
                                "transform": "translateY(-3px)",
                                "box_shadow": "0 0 40px rgba(0,229,255,0.5), 0 8px 30px rgba(0,0,0,0.5)",
                            },
                        ),

                        rx.hstack(
                            rx.text("No profile?", size="1", color="#7fb9d0"),
                            rx.link("Register Identity →", href="/signup", color=PRIMARY_CYAN, weight="bold", size="1",
                                    font_family="Orbitron, sans-serif", _hover={"opacity": "0.7"}),
                            justify="center", spacing="2", margin_top="1.5em",
                        ),

                        rx.html('<div style="width:100%;height:1px;background:rgba(255,255,255,0.05);margin:1.5em 0;"></div>'),
                        rx.link(
                            rx.hstack(
                                rx.icon(tag="arrow-left", size=12),
                                rx.text("RETURN TO HUB", size="1", weight="bold", letter_spacing="1px"),
                                align="center", spacing="1",
                            ),
                            href="/",
                            color="#64acca", font_family="Orbitron, sans-serif",
                            _hover={"color": PRIMARY_CYAN}, transition="color 0.3s ease",
                        ),

                        width="58%", padding="4em", align="center", justify="center", spacing="0",
                    ),

                    class_name="glass-panel glass-panel-cyan card-entry holo-border",
                    border_radius="24px", width="min(1000px, 96vw)",
                    align_items="stretch", spacing="0", overflow="hidden",
                ),
                width="100%", display="flex", justify_content="center", align_items="center",
            ),
            width="100vw", height="100vh",
        ),
        overflow="hidden", width="100%", height="100%",
        on_mount=LoginState.reset_form,
    )
