import reflex as rx

# Logo color scheme from the image
PRIMARY_COLOR = "#0EA5E9"  # Cyan-blue from logo
DARK_BG = "#0a0e27"
ACCENT_COLOR = "#06B6D4"  # Turquoise accent

def feature_card(icon: str, title: str, desc: str):
    """Reusable card for project details with enhanced styling."""
    return rx.vstack(
        # Icon with glow effect
        rx.box(
            rx.icon(tag=icon, size=40, color=PRIMARY_COLOR),
            padding="1em",
            background=f"rgba(14, 165, 233, 0.1)",
            border_radius="12px",
            box_shadow=f"0 0 20px rgba(14, 165, 233, 0.2)",
        ),
        rx.heading(title, size="4", color="#ffffff", weight="bold"),
        rx.text(desc, size="2", color="#b0b0b0", line_height="1.6"),
        align="start",
        padding="2.5em",
        background="rgba(255, 255, 255, 0.05)",
        border=f"1px solid rgba(14, 165, 233, 0.15)",
        border_radius="20px",
        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "transform": "translateY(-15px)",
            "border": f"1px solid rgba(14, 165, 233, 0.4)",
            "background": "rgba(255, 255, 255, 0.08)",
            "box_shadow": f"0 20px 40px rgba(14, 165, 233, 0.15)",
        },
        spacing="3",
    )

def benefit_item(number: str, title: str, desc: str):
    """Reusable benefit item for landing page."""
    return rx.hstack(
        rx.box(
            rx.text(number, size="3", weight="bold", color=PRIMARY_COLOR),
            padding="1.2em",
            background=f"rgba(14, 165, 233, 0.15)",
            border_radius="50%",
            width="60px",
            text_align="center",
            box_shadow=f"0 0 20px rgba(14, 165, 233, 0.2)",
        ),
        rx.vstack(
            rx.heading(title, size="3", color="white", weight="bold"),
            rx.text(desc, size="2", color="#b0b0b0"),
            align="start",
            spacing="1",
        ),
        align="start",
        spacing="4",
        padding="2em",
        background="rgba(255, 255, 255, 0.03)",
        border_left=f"3px solid {PRIMARY_COLOR}",
        border_radius="10px",
    )

def stat_card(number: str, label: str):
    """Reusable stat card for metrics."""
    return rx.vstack(
        rx.heading(
            number,
            size="6",
            color=PRIMARY_COLOR,
            weight="bold",
            style={"text-shadow": f"0 0 20px rgba(14, 165, 233, 0.4)"}
        ),
        rx.text(label, size="2", color="#888", weight="bold", letter_spacing="2px"),
        align="center",
        padding="2em",
        background=f"rgba(14, 165, 233, 0.05)",
        border=f"1px solid rgba(14, 165, 233, 0.15)",
        border_radius="15px",
        spacing="2",
    )

def entry_page() -> rx.Component:
    return rx.box(
        # ANIMATED BACKGROUND ELEMENTS
        rx.box(
            position="fixed",
            width="100vw",
            height="100vh",
            background="linear-gradient(135deg, #0a0e27 0%, #16213e 50%, #0f3460 100%)",
            z_index="-2",
        ),
        
        # FLOATING ORB ANIMATIONS with logo colors
        rx.box(
            position="fixed",
            top="10%",
            left="10%",
            width="400px",
            height="400px",
            background=f"radial-gradient(circle, rgba(14, 165, 233, 0.15) 0%, transparent 70%)",
            border_radius="50%",
            filter="blur(120px)",
            z_index="-1",
            class_name="animate-pulse",
        ),
        
        rx.box(
            position="fixed",
            bottom="5%",
            right="10%",
            width="500px",
            height="500px",
            background=f"radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%)",
            border_radius="50%",
            filter="blur(140px)",
            z_index="-1",
            class_name="animate-pulse",
        ),
        
        # NAVIGATION BAR with LOGO - FIXED AT TOP
        rx.box(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.png",
                        width="50px",
                        height="auto",
                    ),
                    rx.heading("ALETHEIA", size="5", color=PRIMARY_COLOR, weight="bold", style={"letter-spacing": "3px"}),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.link("Features", href="#features", color="#888", _hover={"color": PRIMARY_COLOR}, size="2", weight="bold"),
                    rx.link("Benefits", href="#benefits", color="#888", _hover={"color": PRIMARY_COLOR}, size="2", weight="bold"),
                    rx.link("Security", href="#security", color="#888", _hover={"color": PRIMARY_COLOR}, size="2", weight="bold"),
                    rx.button("Get Access", size="2", background=f"linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR})", color="white", padding_x="2em"),
                    spacing="4",
                ),
                padding="2em 4em",
                background="rgba(0, 0, 0, 0.5)",
                backdrop_filter="blur(10px)",
                border_bottom=f"1px solid rgba(14, 165, 233, 0.2)",
                width="100%",
                align="center",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            z_index="1000",
            width="100%",
        ),
        
        rx.scroll_area(
            rx.vstack(
                # --- HERO SECTION ---
                rx.vstack(
                    # Enhanced logo with glow
                    rx.box(
                        rx.image(
                            src="/logo.png",
                            width="280px",
                            height="auto",
                            class_name="animate__animated animate__fadeInDown",
                        ),
                        filter=f"drop-shadow(0 0 40px rgba(14, 165, 233, 0.6))",
                    ),
                    
                    # Main heading
                    rx.heading(
                        "ALETHEIA GATE",
                        size="9",
                        weight="bold",
                        color="white",
                        style={
                            "letter-spacing": "12px",
                            "text-shadow": f"0 0 30px rgba(14, 165, 233, 0.6), 0 0 60px rgba(6, 182, 212, 0.3)",
                            "font-weight": "900",
                            "background": f"linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR})",
                            "-webkit-background-clip": "text",
                            "-webkit-text-fill-color": "transparent",
                            "background-clip": "text",
                        }
                    ),
                    
                    # Subtitle with animation
                    rx.vstack(
                        rx.text(
                            "UNLOCK TRUTH THROUGH ADVANCED INFORMATION SYSTEMS",
                            color=PRIMARY_COLOR,
                            size="2",
                            style={
                                "letter-spacing": "5px",
                                "font-weight": "600",
                                "text-shadow": f"0 0 15px rgba(14, 165, 233, 0.4)",
                            }
                        ),
                        rx.box(
                            height="2px",
                            width="250px",
                            background=f"linear-gradient(90deg, transparent, {PRIMARY_COLOR}, transparent)",
                        ),
                        align="center",
                        spacing="2",
                    ),
                    
                    # CTA Description
                    rx.text(
                        "Enterprise-grade decentralized infrastructure for secure data management and truth verification in the digital age.",
                        size="3",
                        color="#b0b0b0",
                        text_align="center",
                        max_width="700px",
                        line_height="1.8",
                    ),
                    
                    # CTA BUTTONS
                    rx.hstack(
                        rx.button(
                            "Launch Application",
                            size="3",
                            weight="bold",
                            padding="1.5em 3em",
                            background=f"linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR})",
                            color="white",
                            border_radius="10px",
                            letter_spacing="2px",
                            transition="all 0.4s ease",
                            _hover={
                                "transform": "translateY(-5px)",
                                "box_shadow": f"0 20px 50px rgba(14, 165, 233, 0.3)",
                            },
                            on_click=rx.redirect("/hub")
                        ),
                        rx.button(
                            "Learn More",
                            size="3",
                            weight="bold",
                            padding="1.5em 3em",
                            background="transparent",
                            color=PRIMARY_COLOR,
                            border=f"2px solid {PRIMARY_COLOR}",
                            border_radius="10px",
                            letter_spacing="2px",
                            transition="all 0.4s ease",
                            _hover={
                                "transform": "translateY(-5px)",
                                "background": "rgba(14, 165, 233, 0.1)",
                                "box_shadow": f"0 20px 50px rgba(14, 165, 233, 0.2)",
                            },
                        ),
                        spacing="4",
                        padding_top="2em",
                    ),
                    
                    height="100vh",
                    justify="center",
                    align="center",
                    spacing="8",
                    padding_x="2em",
                ),
                
                # --- STATS SECTION ---
                rx.vstack(
                    rx.grid(
                        stat_card("99.9%", "UPTIME"),
                        stat_card("256-bit", "ENCRYPTION"),
                        stat_card("∞", "SCALABILITY"),
                        stat_card("24/7", "SUPPORT"),
                        columns="4",
                        spacing="4",
                        width="100%",
                        max_width="900px",
                    ),
                    padding_y="8vh",
                    padding_x="2em",
                    width="100%",
                    align="center",
                ),
                
                # --- FEATURES SECTION ---
                rx.vstack(
                    rx.vstack(
                        rx.heading(
                            "CORE FEATURES",
                            id="features",
                            size="7",
                            color="white",
                            weight="bold",
                            style={"letter-spacing": "3px"}
                        ),
                        rx.text(
                            "Powered by cutting-edge technology and security protocols",
                            size="2",
                            color="#888",
                        ),
                        align="center",
                        spacing="2",
                        padding_bottom="3em",
                    ),
                    
                    rx.grid(
                        feature_card("database", "Surreal Core", "Multi-model graph database for hyper-relational truth tracking and real-time data synchronization."),
                        feature_card("shield", "End-to-End Encryption", "Quantum-resistant encryption for every data packet across the gate with military-grade protocols."),
                        feature_card("cpu", "Neural Logic", "AI-driven unconcealment filters to separate signal from noise with advanced ML algorithms."),
                        feature_card("globe", "Global Node Mesh", "Decentralized network ensuring 99.9% uptime across continents with redundancy."),
                        feature_card("lock", "Zero-Trust Security", "Never trust, always verify approach to access control and data validation."),
                        feature_card("zap", "Lightning-Fast", "Sub-millisecond response times with edge computing distribution."),
                        columns="3",
                        spacing="6",
                        width="100%",
                        max_width="1200px",
                    ),
                    
                    padding_y="10vh",
                    padding_x="2em",
                    width="100%",
                    align="center",
                ),
                
                # --- BENEFITS SECTION ---
                rx.vstack(
                    rx.vstack(
                        rx.heading(
                            "WHY CHOOSE ALETHEIA",
                            id="benefits",
                            size="7",
                            color="white",
                            weight="bold",
                            style={"letter-spacing": "3px"}
                        ),
                        rx.text(
                            "Experience the future of secure information management",
                            size="2",
                            color="#888",
                        ),
                        align="center",
                        spacing="2",
                        padding_bottom="3em",
                    ),
                    
                    rx.vstack(
                        benefit_item("1", "Enterprise-Grade Security", "Bank-level encryption and security protocols to keep your data safe from threats."),
                        benefit_item("2", "Infinite Scalability", "Grow without limits. Our architecture scales horizontally across unlimited nodes."),
                        benefit_item("3", "Global Distribution", "Deploy anywhere in the world with automatic replication and disaster recovery."),
                        benefit_item("4", "Developer-Friendly API", "Comprehensive REST and GraphQL APIs with SDKs for every major language."),
                        benefit_item("5", "24/7 Expert Support", "Round-the-clock support from our team of security and infrastructure experts."),
                        benefit_item("6", "Compliance Ready", "GDPR, HIPAA, SOC2, and ISO 27001 compliant infrastructure."),
                        spacing="4",
                        width="100%",
                        max_width="800px",
                    ),
                    
                    padding_y="10vh",
                    padding_x="2em",
                    width="100%",
                    align="center",
                ),
                
                # --- SECURITY SECTION ---
                rx.vstack(
                    rx.vstack(
                        rx.heading(
                            "SECURITY & COMPLIANCE",
                            id="security",
                            size="7",
                            color="white",
                            weight="bold",
                            style={"letter-spacing": "3px"}
                        ),
                        rx.text(
                            "Built with security as the foundation, not an afterthought",
                            size="2",
                            color="#888",
                        ),
                        align="center",
                        spacing="2",
                        padding_bottom="3em",
                    ),
                    
                    rx.grid(
                        rx.vstack(
                            rx.icon(tag="shield-check", size=50, color=PRIMARY_COLOR),
                            rx.heading("Quantum-Safe", size="4", color="white", weight="bold"),
                            rx.text("Post-quantum cryptography ready for tomorrow's threats", size="2", color="#888", text_align="center"),
                            align="center",
                            padding="2em",
                        ),
                        rx.vstack(
                            rx.icon(tag="lock", size=50, color=PRIMARY_COLOR),
                            rx.heading("Zero-Knowledge Proof", size="4", color="white", weight="bold"),
                            rx.text("Verify without revealing sensitive information", size="2", color="#888", text_align="center"),
                            align="center",
                            padding="2em",
                        ),
                        rx.vstack(
                            rx.icon(tag="audit", size=50, color=PRIMARY_COLOR),
                            rx.heading("Full Audit Trails", size="4", color="white", weight="bold"),
                            rx.text("Complete immutable logs of all operations and access", size="2", color="#888", text_align="center"),
                            align="center",
                            padding="2em",
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
                        max_width="1000px",
                    ),
                    
                    padding_y="10vh",
                    padding_x="2em",
                    width="100%",
                    align="center",
                ),
                
                # --- CTA SECTION ---
                rx.vstack(
                    rx.heading(
                        "Ready to Unlock the Truth?",
                        size="8",
                        color="white",
                        weight="bold",
                        text_align="center",
                    ),
                    rx.text(
                        "Join enterprises worldwide securing their most critical information with Aletheia Gate.",
                        size="3",
                        color="#b0b0b0",
                        text_align="center",
                        max_width="600px",
                    ),
                    rx.hstack(
                        rx.button(
                            "Start Free Trial",
                            size="3",
                            weight="bold",
                            padding="1.5em 3em",
                            background=f"linear-gradient(135deg, {PRIMARY_COLOR}, {ACCENT_COLOR})",
                            color="white",
                            border_radius="10px",
                            letter_spacing="2px",
                            _hover={
                                "transform": "translateY(-3px)",
                                "box_shadow": f"0 20px 50px rgba(14, 165, 233, 0.3)",
                            },
                        ),
                        spacing="4",
                    ),
                    padding_y="12vh",
                    padding_x="2em",
                    width="100%",
                    align="center",
                    spacing="4",
                    background=f"rgba(14, 165, 233, 0.05)",
                    border_top=f"1px solid rgba(14, 165, 233, 0.1)",
                    border_bottom=f"1px solid rgba(14, 165, 233, 0.1)",
                ),
                
                # FOOTER
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.heading("ALETHEIA", size="4", color=PRIMARY_COLOR, weight="bold"),
                            rx.text("Unlocking truth through advanced systems", size="2", color="#888"),
                            align="start",
                        ),
                        rx.spacer(),
                        rx.vstack(
                            rx.text("PRODUCT", size="2", color=PRIMARY_COLOR, weight="bold"),
                            rx.link("Features", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Pricing", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Security", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            align="start",
                            spacing="3",
                        ),
                        rx.vstack(
                            rx.text("COMPANY", size="2", color=PRIMARY_COLOR, weight="bold"),
                            rx.link("About", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Blog", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Careers", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            align="start",
                            spacing="3",
                        ),
                        rx.vstack(
                            rx.text("LEGAL", size="2", color=PRIMARY_COLOR, weight="bold"),
                            rx.link("Privacy", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Terms", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            rx.link("Contact", href="#", color="#888", size="2", _hover={"color": PRIMARY_COLOR}),
                            align="start",
                            spacing="3",
                        ),
                        width="100%",
                        spacing="8",
                        padding_bottom="2em",
                        border_bottom=f"1px solid rgba(14, 165, 233, 0.1)",
                    ),
                    rx.hstack(
                        rx.text("© 2026 ALETHEIA GATE. All rights reserved.", size="1", color="#555"),
                        rx.spacer(),
                        rx.text("Protocol Status: ACTIVE | Data Integrity: VERIFIED | Network: SECURE", size="1", color="#444"),
                        width="100%",
                        align="center",
                        padding_top="2em",
                    ),
                    padding="6em 4em",
                    width="100%",
                    align="center",
                    spacing="4",
                ),
                
                width="100%",
                align="center",
                padding_top="80px",
            ),
            width="100%",
        ),
        
        width="100%",
        height="100%",
        overflow_x="hidden",
    )