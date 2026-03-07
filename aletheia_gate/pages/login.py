import reflex as rx

# Color scheme - CYAN for login
PRIMARY_COLOR = "#00E5FF"  # Terminal Cyan
DARK_BG = "#0B0F1A"  # Deep space black

def login_page() -> rx.Component:
    """Login page with diagonal split design - Cyan theme"""
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
        
        # Ambient glow - CYAN on left
        rx.box(
            position="fixed",
            top="50%",
            left="20%",
            transform="translate(-50%, -50%)",
            width="500px",
            height="500px",
            background=f"radial-gradient(circle, rgba(0, 229, 255, 0.2) 0%, transparent 70%)",
            border_radius="50%",
            filter="blur(80px)",
            z_index="-1",
        ),
        
        # Main container
        rx.vstack(
            # Split Card Container
            rx.box(
                rx.hstack(
                    # LEFT SIDE - Login Form (Dark/Cyan)
                    rx.vstack(
                        rx.heading(
                            "Login",
                            size="5",
                            color="white",
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                        ),
                        
                        # Username
                        rx.vstack(
                            rx.text("Username", size="2", color="#888", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Enter your username",
                                type="text",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(0, 229, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(0, 229, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Password
                        rx.vstack(
                            rx.text("Password", size="2", color="#888", weight="bold", font_family="Exo 2, sans-serif"),
                            rx.input(
                                placeholder="Enter your password",
                                type="password",
                                width="100%",
                                padding="0.8em 1em",
                                background="rgba(0, 0, 0, 0.6)",
                                border=f"1px solid rgba(0, 229, 255, 0.3)",
                                color="white",
                                border_radius="6px",
                                font_family="JetBrains Mono, monospace",
                                _focus={
                                    "border_color": PRIMARY_COLOR,
                                    "box_shadow": f"0 0 15px rgba(0, 229, 255, 0.3)",
                                }
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        
                        # Login button with cyan glow
                        rx.button(
                            "Login",
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
                                "background": f"rgba(0, 229, 255, 0.1)",
                                "box_shadow": f"0 0 20px rgba(0, 229, 255, 0.4)",
                            }
                        ),
                        
                        # Sign up link
                        rx.hstack(
                            rx.text("Don't have an account?", size="2", color="#888", font_family="Exo 2, sans-serif"),
                            rx.link(
                                "Sign Up",
                                href="/signup",
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
                        spacing="3",
                        padding="3em 2.5em",
                        width="50%",
                        justify="center",
                    ),
                    
                    # RIGHT SIDE - Welcome message (Cyan gradient)
                    rx.vstack(
                        rx.heading(
                            "WELCOME",
                            size="5",
                            color="white",
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                        ),
                        rx.heading(
                            "BACK!",
                            size="5",
                            color=PRIMARY_COLOR,
                            weight="bold",
                            font_family="Orbitron, sans-serif",
                            letter_spacing="2px",
                            margin_top="-0.6em",
                        ),
                        rx.text(
                            "We're happy to see you again. Access all your data and stay connected.",
                            size="3",
                            color="#d0d0d0",
                            text_align="center",
                            line_height="1.6",
                            font_family="Exo 2, sans-serif",
                        ),
                        align="center",
                        justify="center",
                        spacing="2",
                        padding="3em 2.5em",
                        width="50%",
                        background=f"linear-gradient(135deg, rgba(0, 229, 255, 0.15) 0%, rgba(0, 229, 255, 0.08) 100%)",
                        position="relative",
                    ),
                    
                    spacing="0",
                    width="100%",
                    height="100%",
                ),
                
                border=f"2px solid rgba(0, 229, 255, 0.4)",
                border_radius="15px",
                overflow="hidden",
                background="rgba(20, 26, 46, 0.7)",
                width="95%",
                max_width="800px",
                height="350px",
                box_shadow=f"0 0 40px rgba(0, 229, 255, 0.25)",
            ),
            
            # Back button
            rx.link(
                "← Back to Home",
                href="/",
                size="2",
                color=PRIMARY_COLOR,
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
