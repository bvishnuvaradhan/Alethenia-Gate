import reflex as rx
import re

PRIMARY_PURPLE = "#C44CFF"
DARK_BG = "#0B0F1A"
VERIFIED_GREEN = "#00FF9C"
ERROR_RED = "#FF4D6D"


class SignupState(rx.State):
    name: str = ""
    email: str = ""
    password: str = ""
    name_error: str = ""
    email_error: str = ""
    password_error: str = ""
    success: bool = False

    def reset_form(self):
        """Clear form on page load so previous inputs don't persist."""
        self.name = ""
        self.email = ""
        self.password = ""
        self.name_error = ""
        self.email_error = ""
        self.password_error = ""
        self.success = False

    def set_name(self, value: str):
        self.name = value
        if self.name_error:
            self.name_error = ""

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
        if not self.name.strip():
            self.name_error = "Full name is required."
            valid = False
        elif len(self.name.strip()) < 2:
            self.name_error = "Name must be at least 2 characters."
            valid = False
        if not self.email:
            self.email_error = "Email is required."
            valid = False
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.email_error = "Enter a valid email address."
            valid = False
        if not self.password:
            self.password_error = "Password is required."
            valid = False
        elif len(self.password) < 8:
            self.password_error = "Password must be at least 8 characters."
            valid = False
        return valid

    def handle_signup(self):
        self.success = False
        if self.validate():
            # On success → redirect to hub
            return rx.redirect("/hub")

    def handle_enter(self, key: str):
        """Submit on Enter key press."""
        if key == "Enter":
            return self.handle_signup()


def _glitch_heading_purple(text: str, is_gradient: bool = False) -> rx.Component:
    cls = "glitch-wrapper gradient-text-purple" if is_gradient else "glitch-wrapper"
    color = "transparent" if is_gradient else "white"
    return rx.html(
        f'<div class="{cls}" data-text="{text}" style="font-size:3rem;font-weight:900;font-family:Orbitron,sans-serif;letter-spacing:4px;color:{color};line-height:1;">{text}</div>'
    )


def _data_lines_purple() -> rx.Component:
    lines = [
        ("REGISTER::ID", "5%", "0.5s", "2"),
        ("10110011", "30%", "1.5s", "2.5"),
        ("ENCRYPT//ON", "55%", "0.8s", "3"),
        ("11001100", "75%", "2s", "2"),
        ("VAULT::INIT", "90%", "0.2s", "3.5"),
    ]
    return rx.box(
        *[
            rx.html(
                f'<div class="data-stream-line" style="left:{l};animation-delay:{d}s;animation-duration:{dur}s;color:rgba(196,76,255,0.2);">{t}</div>'
            )
            for t, l, d, dur in lines
        ],
        position="absolute", inset="0", overflow="hidden", pointer_events="none",
    )


def _error_msg(msg: rx.Var) -> rx.Component:
    return rx.cond(
        msg != "",
        rx.hstack(
            rx.icon(tag="circle-alert", size=12, color=ERROR_RED),
            rx.text(msg, size="1", color=ERROR_RED, font_family="Exo 2, sans-serif"),
            spacing="1", align="center", margin_top="0.3em",
        ),
    )


def signup_page() -> rx.Component:
    return rx.box(
        rx.box(
            position="fixed", inset="0",
            background=DARK_BG, class_name="neural-grid", z_index="-3",
        ),
        rx.box(
            position="fixed", top="-10%", right="-10%",
            width="600px", height="600px",
            background="radial-gradient(circle, rgba(196,76,255,0.10) 0%, transparent 70%)",
            border_radius="50%", filter="blur(100px)", z_index="-2", class_name="animate-pulse",
        ),
        rx.box(
            position="fixed", bottom="-10%", left="-10%",
            width="500px", height="500px",
            background="radial-gradient(circle, rgba(0,229,255,0.06) 0%, transparent 70%)",
            border_radius="50%", filter="blur(100px)", z_index="-2",
        ),

        rx.center(
            rx.box(
                rx.hstack(
                    # === LEFT PANEL ===
                    rx.box(
                        rx.box(class_name="noise-bg"),
                        rx.html('<div class="scanline" style="background:linear-gradient(to right,transparent,rgba(196,76,255,0.3),transparent);"></div>'),
                        _data_lines_purple(),
                        _glitch_heading_purple("JOIN THE"),
                        _glitch_heading_purple("GATE", is_gradient=True),

                        rx.hstack(
                            rx.box(width="8px", height="8px", background=VERIFIED_GREEN,
                                   border_radius="50%", class_name="verified-pulse fast-glow"),
                            rx.text("REGISTRATION OPEN", size="1", color=VERIFIED_GREEN, weight="bold",
                                    letter_spacing="2px", font_family="JetBrains Mono, monospace"),
                            align="center", spacing="2", margin_top="1.5em",
                        ),
                        rx.html('<div style="width:60%;height:1px;background:linear-gradient(to right,transparent,rgba(196,76,255,0.4),transparent);margin:1.5em auto;"></div>'),

                        rx.vstack(
                            rx.hstack(
                                rx.box(rx.icon(tag="shield-check", size=16, color=VERIFIED_GREEN), class_name="fast-glow"),
                                rx.text("Quantum-Safe Security", size="2", color="#94A3B8", font_family="Exo 2, sans-serif"),
                                spacing="3", align="center",
                            ),
                            rx.hstack(
                                rx.box(rx.icon(tag="globe", size=16, color=VERIFIED_GREEN), class_name="fast-glow"),
                                rx.text("Global Intelligence Access", size="2", color="#94A3B8", font_family="Exo 2, sans-serif"),
                                spacing="3", align="center",
                            ),
                            rx.hstack(
                                rx.box(rx.icon(tag="zap", size=16, color=VERIFIED_GREEN), class_name="fast-glow"),
                                rx.text("Real-time Insight Stream", size="2", color="#94A3B8", font_family="Exo 2, sans-serif"),
                                spacing="3", align="center",
                            ),
                            align="start", spacing="3", margin_top="1em",
                        ),

                        display="flex", flex_direction="column",
                        align_items="center", justify_content="center",
                        width="42%", background="rgba(0,0,0,0.45)",
                        position="relative", overflow="hidden", padding="4em 2em",
                    ),

                    # === RIGHT PANEL: FORM ===
                    rx.vstack(
                        rx.vstack(
                            rx.html('<div style="font-size:1.4rem;font-weight:900;font-family:Orbitron,sans-serif;letter-spacing:2px;color:white;">Identity Registration</div>'),
                            rx.text("Create your secure neural profile", size="1", color="#b07fcf", font_family="Exo 2, sans-serif"),
                            align="center", spacing="1", margin_bottom="1.5em",
                        ),

                        # Success banner
                        rx.cond(
                            SignupState.success,
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="check-circle", size=14, color=VERIFIED_GREEN),
                                    rx.text("Registration successful! Redirecting...", size="1", color=VERIFIED_GREEN, weight="bold"),
                                    spacing="2", align="center",
                                ),
                                width="100%", padding="0.8em 1.2em",
                                background="rgba(0,255,156,0.08)",
                                border="1px solid rgba(0,255,156,0.3)",
                                border_radius="10px", margin_bottom="0.5em",
                            ),
                        ),

                        rx.scroll_area(
                            rx.vstack(
                                # Name field
                                rx.vstack(
                                    rx.text("LEGAL NAME", size="1", color=PRIMARY_PURPLE, weight="bold", letter_spacing="2px", font_family="Orbitron, sans-serif"),
                                    rx.input(
                                        placeholder="Enter full name",
                                        type="text",
                                        value=SignupState.name,
                                        on_change=SignupState.set_name,
                                        width="100%", height="3.2em",
                                        background="rgba(8,14,30,0.8)",
                                        border=rx.cond(
                                            SignupState.name_error != "",
                                            f"1px solid {ERROR_RED}",
                                            "1px solid rgba(196,76,255,0.15)",
                                        ),
                                        color="white", padding_x="1.5em", border_radius="12px",
                                        font_family="JetBrains Mono, monospace",
                                        _focus={"border_color": PRIMARY_PURPLE, "box_shadow": "0 0 25px rgba(196,76,255,0.25)"},
                                        on_key_down=SignupState.handle_enter,
                                    ),
                                    _error_msg(SignupState.name_error),
                                    spacing="1", width="100%",
                                ),
                                # Email field
                                rx.vstack(
                                    rx.text("NEURAL EMAIL", size="1", color=PRIMARY_PURPLE, weight="bold", letter_spacing="2px", font_family="Orbitron, sans-serif"),
                                    rx.input(
                                        placeholder="system@email.ext",
                                        type="email",
                                        value=SignupState.email,
                                        on_change=SignupState.set_email,
                                        width="100%", height="3.2em",
                                        background="rgba(8,14,30,0.8)",
                                        border=rx.cond(
                                            SignupState.email_error != "",
                                            f"1px solid {ERROR_RED}",
                                            "1px solid rgba(196,76,255,0.15)",
                                        ),
                                        color="white", padding_x="1.5em", border_radius="12px",
                                        font_family="JetBrains Mono, monospace",
                                        _focus={"border_color": PRIMARY_PURPLE, "box_shadow": "0 0 25px rgba(196,76,255,0.25)"},
                                        on_key_down=SignupState.handle_enter,
                                    ),
                                    _error_msg(SignupState.email_error),
                                    spacing="1", width="100%",
                                ),
                                # Password field
                                rx.vstack(
                                    rx.text("ACCESS PASSCODE", size="1", color=PRIMARY_PURPLE, weight="bold", letter_spacing="2px", font_family="Orbitron, sans-serif"),
                                    rx.input(
                                        placeholder="Min. 8 characters",
                                        type="password",
                                        value=SignupState.password,
                                        on_change=SignupState.set_password,
                                        width="100%", height="3.2em",
                                        background="rgba(8,14,30,0.8)",
                                        border=rx.cond(
                                            SignupState.password_error != "",
                                            f"1px solid {ERROR_RED}",
                                            "1px solid rgba(196,76,255,0.15)",
                                        ),
                                        color="white", padding_x="1.5em", border_radius="12px",
                                        font_family="JetBrains Mono, monospace",
                                        _focus={"border_color": PRIMARY_PURPLE, "box_shadow": "0 0 25px rgba(196,76,255,0.25)"},
                                        on_key_down=SignupState.handle_enter,
                                    ),
                                    _error_msg(SignupState.password_error),
                                    spacing="1", width="100%",
                                ),
                                spacing="4", width="100%",
                            ),
                            max_height="300px", width="100%",
                        ),

                        rx.button(
                            "Register Identity",
                            on_click=SignupState.handle_signup,
                            width="100%", height="3.4em",
                            background=f"linear-gradient(135deg, {PRIMARY_PURPLE}, #7000ff)",
                            color="white", border="none", border_radius="12px",
                            font_family="Orbitron, sans-serif", font_weight="900",
                            letter_spacing="3px", font_size="0.85rem",
                            cursor="pointer", margin_top="1.5em",
                            box_shadow="0 0 20px rgba(196,76,255,0.3), 0 4px 15px rgba(0,0,0,0.4)",
                            transition="all 0.4s ease",
                            _hover={
                                "transform": "translateY(-3px)",
                                "box_shadow": "0 0 40px rgba(196,76,255,0.5), 0 8px 30px rgba(0,0,0,0.5)",
                            },
                        ),

                        rx.hstack(
                            rx.text("Already registered?", size="1", color="#b07fcf"),
                            rx.link("Initiate Access →", href="/login", color=PRIMARY_PURPLE, weight="bold", size="1",
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
                            color="#b07fcf", font_family="Orbitron, sans-serif",
                            _hover={"color": PRIMARY_PURPLE}, transition="color 0.3s ease",
                        ),

                        width="58%", padding="4em", align="center", justify="center", spacing="0",
                    ),

                    class_name="glass-panel glass-panel-purple card-entry holo-border",
                    border_radius="24px", width="min(1000px, 96vw)",
                    align_items="stretch", spacing="0", overflow="hidden",
                ),
                width="100%", display="flex", justify_content="center", align_items="center",
            ),
            width="100vw", height="100vh",
        ),
        overflow="hidden", width="100%", height="100%",
        on_mount=SignupState.reset_form,
    )
