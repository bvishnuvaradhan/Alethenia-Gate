import reflex as rx

# Color scheme - PURPLE for signup
PRIMARY_COLOR = "#C44CFF"  # Purple
CYAN_COLOR = "#00E5FF"  # Terminal Cyan
DARK_BG = "#0B0F1A"  # Deep space black
VERIFIED_GREEN = "#00FF9C"  # Success green

def signup_page() -> rx.Component:
    """Signup page with diagonal split design - Purple theme"""
    return rx.box(
        # Background
        rx.box(
            position="fixed",
            width="100vw",
            height="100vh",
            background=DARK_BG,
            class_name="neural-grid",
            z_index="-2",
        ),
        
        # Ambient glow - PURPLE on right
        rx.box(
            position="fixed",
            top="50%",
            right="20%",
            transform="translate(50%, -50%)",
            width="500px",
            height="500px",
            background=f"radial-gradient(circle, rgba(196, 76, 255, 0.2) 0%, transparent 70%)",
            border_radius="50%",
            filter="blur(80px)",
            z_index="-1",
        ),
        
        # Main container
        rx.vstack(
            # Split Card Container
            rx.box(
                rx.hstack(
                    # LEFT SIDE - Registration Form (Purple)
                    rx.vstack(
                        rx.heading(
                            "Sign Up",
                            size="5",
                            color="white",
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                        ),
                        
                        # Full name
                        rx.vstack(
                            rx.text("Full Name", size="2", color="#ccc", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Your full name",
                                type="text",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(196, 76, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(196, 76, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Email
                        rx.vstack(
                            rx.text("Email", size="2", color="#ccc", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="your@email.com",
                                type="email",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(196, 76, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(196, 76, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Username
                        rx.vstack(
                            rx.text("Username", size="2", color="#ccc", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Choose a username",
                                type="text",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(196, 76, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(196, 76, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Password
                        rx.vstack(
                            rx.text("Password", size="2", color="#ccc", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Create a strong password",
                                type="password",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(196, 76, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(196, 76, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Confirm Password
                        rx.vstack(
                            rx.text("Confirm Password", size="2", color="#ccc", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Confirm your password",
                                type="password",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(196, 76, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(196, 76, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Sign up button with purple glow
                        rx.button(
                            "Create Account",
                            width="100%",
                            padding="1em",
                            background="transparent",
                            color=PRIMARY_COLOR,
                            border=f"2px solid {PRIMARY_COLOR}",
                            border_radius="8px",
                            font_family="Orbitron, sans-serif",
                            weight="bold",
                            letter_spacing="1px",
                            class_name="glow-shadow-hover",
                            _hover={
                                "background": f"rgba(196, 76, 255, 0.1)",
                                "box_shadow": f"0 0 20px rgba(196, 76, 255, 0.4)",
                            }
                        ),
                        
                        # Login link
                        rx.hstack(
                            rx.text("Already have an account?", size="2", color="#888", font_family="Exo 2, sans-serif"),
                            rx.link(
                                "Login",
                                href="/login",
                                size="2",
                                color=PRIMARY_COLOR,
                                weight="bold",
                                _hover={"text_decoration": "underline"},
                                font_family="Exo 2, sans-serif",
                            ),
                            justify="center",
                            spacing="1",
                        ),
                        
                        align="center",
                        spacing="2",
                        padding="2.5em 2em",
                        width="50%",
                        justify="center",
                    ),
                    
                    # RIGHT SIDE - Benefits message (Cyan gradient)
                    rx.vstack(
                        rx.heading(
                            "JOIN THE",
                            size="5",
                            color=CYAN_COLOR,
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                        ),
                        rx.heading(
                            "NETWORK",
                            size="5",
                            color="white",
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                            margin_top="-0.6em",
                        ),
                        rx.text(
                            "Unlock enterprise-grade security and intelligence verification.",
                            size="3",
                            color="#d0d0d0",
                            text_align="center",
                            line_height="1.6",
                            font_family="Exo 2, sans-serif",
                        ),
                        
                        # Benefits checklist
                        rx.vstack(
                            rx.hstack(
                                rx.text("✓", size="4", color=VERIFIED_GREEN, weight="bold"),
                                rx.text("Advanced Verification", size="2", color="#d0d0d0", font_family="Exo 2, sans-serif"),
                                spacing="1",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("✓", size="4", color=VERIFIED_GREEN, weight="bold"),
                                rx.text("Global Intelligence Access", size="2", color="#d0d0d0", font_family="Exo 2, sans-serif"),
                                spacing="1",
                                align="center",
                            ),
                            rx.hstack(
                                rx.text("✓", size="4", color=VERIFIED_GREEN, weight="bold"),
                                rx.text("Real-time Insights", size="2", color="#d0d0d0", font_family="Exo 2, sans-serif"),
                                spacing="1",
                                align="center",
                            ),
                            spacing="1",
                            margin_top="1.5em",
                        ),
                        
                        align="center",
                        justify="center",
                        spacing="3",
                        padding="2.5em 2em",
                        width="50%",
                        background=f"linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(0, 229, 255, 0.08) 100%)",
                        position="relative",
                    ),
                    
                    spacing="0",
                    width="100%",
                    height="100%",
                ),
                
                border=f"2px solid rgba(196, 76, 255, 0.4)",
                border_radius="15px",
                overflow="hidden",
                background="rgba(20, 26, 46, 0.7)",
                width="95%",
                max_width="900px",
                height="380px",
                box_shadow=f"0 0 40px rgba(196, 76, 255, 0.25)",
            ),
            
            # Back button
            rx.link(
                "← Back to Home",
                href="/",
                size="2",
                color=CYAN_COLOR,
                weight="bold",
                _hover={"text_decoration": "underline"},
                font_family="Exo 2, sans-serif",
            ),
            
            height="100vh",
            width="100%",
            padding="3em 2em",
            justify="center",
            align="center",
            spacing="3",
        ),
        
        width="100%",
        height="100%",
        overflow="hidden",
    )
