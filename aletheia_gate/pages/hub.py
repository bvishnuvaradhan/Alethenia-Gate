import reflex as rx


class HubState(rx.State):
    """The central state for model scores and system status."""
    gpt_score: str = "94"
    llama_score: str = "78"
    groq_score: str = "85"
    current_query: str = "Detecting logical fallacies in synthetic training data..."
    system_status: str = "OPTIMAL"
    throughput: str = "2.4M tok/min"
    latency: str = "132 ms"
    anomaly_rate: str = "0.8%"


def sidebar_item(icon: str, text: str, url: str, active: bool = False) -> rx.Component:
    """Sidebar navigation item with active state styling."""
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=18, color="#14f1d9" if active else "#8b9ab0"),
            rx.text(
                text,
                size="3",
                weight="medium",
                class_name="font-orbitron",
                color="white" if active else "#8b9ab0",
            ),
            spacing="3",
            padding="14px 20px",
            border_radius="12px",
            class_name=f"hub-sidebar-item {'active' if active else ''}",
            width="100%",
            align_items="center",
        ),
        href=url,
        text_decoration="none",
        width="100%",
    )


def stat_card(label: str, value: str, detail: str, tone: str) -> rx.Component:
    """Compact metric card for real-time telemetry (cinematic)."""
    return rx.vstack(
        rx.hstack(
            rx.text(label, size="1", color="#a8bec8", class_name="font-jetbrains", font_weight="500"),
            rx.spacer(),
            rx.badge(detail, radius="full", variant="soft", color_scheme=tone, size="1"),
            width="100%",
            align_items="center",
        ),
        rx.heading(value, size="5", color="#e8f4f9", class_name="font-orbitron", font_weight="600"),
        class_name="hub-stat-card",
        width="100%",
        spacing="2",
    )


def model_row(model: str, score: str, status: str, color: str) -> rx.Component:
    """Model integrity row with progress bar and status pill."""
    return rx.vstack(
        rx.hstack(
            rx.text(model, color="white", weight="bold"),
            rx.spacer(),
            rx.text(f"{score}%", class_name="font-jetbrains", color="#d7e2eb"),
            rx.badge(status, radius="full", variant="soft", color_scheme=color),
            width="100%",
            align_items="center",
        ),
        rx.box(
            rx.box(
                height="100%",
                width=f"{score}%",
                class_name="hub-progress-fill",
            ),
            class_name="hub-progress-track",
            width="100%",
        ),
        width="100%",
        spacing="2",
    )


def radar_ring_segment(size: str, thickness: str, gradient: str, glow: str) -> rx.Component:
    """A masked conic-gradient ring with segmented neon arcs."""
    return rx.box(
        class_name="radar-ring-segment",
        style={
            "width": size,
            "height": size,
            "--ring-thickness": thickness,
            "--ring-gradient": gradient,
            "--ring-glow": glow,
        },
    )


def radar_track_ring(size: str, thickness: str) -> rx.Component:
    """Muted full-circle track ring behind each colored segment ring."""
    return rx.box(
        class_name="radar-track-ring",
        style={
            "width": size,
            "height": size,
            "--ring-thickness": thickness,
        },
    )


def radar_spoke(rotation: str) -> rx.Component:
    """Thin radial spoke line for the radar scaffold."""
    return rx.box(
        class_name="radar-spoke",
        style={"transform": f"translate(-50%, -50%) rotate({rotation})"},
    )


def hallucination_radar() -> rx.Component:
    """Circular radar with clean tracks, neon segments, and a scanner wedge."""
    return rx.box(
        rx.box(
            rx.box(class_name="radar-grid-bg"),
            rx.box(class_name="radar-circle-shell"),
            radar_track_ring("88%", "11px"),
            radar_track_ring("74%", "11px"),
            radar_track_ring("60%", "11px"),
            radar_track_ring("46%", "11px"),
            radar_track_ring("32%", "11px"),
            radar_spoke("0deg"),
            radar_spoke("45deg"),
            radar_spoke("90deg"),
            radar_spoke("135deg"),
            rx.box(class_name="radar-sweep-circular"),
            radar_ring_segment(
                "88%",
                "11px",
                "conic-gradient(from 10deg, transparent 0 18%, rgba(96, 239, 255, 0.15) 18% 42%, transparent 42% 100%)",
                "rgba(96, 239, 255, 0.6)",
            ),
            radar_ring_segment(
                "74%",
                "11px",
                "conic-gradient(from 85deg, transparent 0 35%, rgba(205, 113, 255, 0.15) 35% 68%, transparent 68% 100%)",
                "rgba(205, 113, 255, 0.6)",
            ),
            radar_ring_segment(
                "60%",
                "11px",
                "conic-gradient(from 165deg, transparent 0 52%, rgba(85, 245, 184, 0.15) 52% 82%, transparent 82% 100%)",
                "rgba(85, 245, 184, 0.6)",
            ),
            radar_ring_segment(
                "46%",
                "11px",
                "conic-gradient(from 220deg, transparent 0 28%, rgba(96, 239, 255, 0.12) 28% 75%, transparent 75% 100%)",
                "rgba(96, 239, 255, 0.55)",
            ),
            radar_ring_segment(
                "32%",
                "11px",
                "conic-gradient(from 295deg, transparent 0 8%, rgba(85, 245, 184, 0.12) 8% 48%, transparent 48% 100%)",
                "rgba(85, 245, 184, 0.55)",
            ),
            rx.box(
                position="absolute",
                top="50%",
                left="50%",
                width="22px",
                height="22px",
                background="#00FF9C",
                border_radius="50%",
                class_name="core-node",
            ),
            class_name="radar-stage",
        ),
        rx.vstack(
            rx.text(f"Truth Probability ({HubState.gpt_score}%)", color="#71f5ff", size="2", weight="bold"),
            rx.text("Orbitron", color="white", size="3", class_name="font-orbitron"),
            class_name="radar-hud-label radar-hud-top-left",
            spacing="1",
            align_items="start",
        ),
        rx.vstack(
            rx.text("Evidence Strength", color="#9fc8d6", size="2", weight="bold"),
            rx.text("JetBrains Mono", color="white", size="3", class_name="font-jetbrains"),
            class_name="radar-hud-label radar-hud-top-right",
            spacing="1",
            align_items="end",
        ),
        rx.vstack(
            rx.text(f"Evidence Strength ({HubState.gpt_score}%)", color="#71f5ff", size="2", weight="bold"),
            rx.text("JetBrains Mono", color="white", size="3", class_name="font-jetbrains"),
            class_name="radar-hud-label radar-hud-bottom-left",
            spacing="1",
            align_items="start",
        ),
        rx.vstack(
            rx.text("Token Reliability", color="#9fc8d6", size="2", weight="bold"),
            rx.text("JetBrains Mono", color="white", size="3", class_name="font-jetbrains"),
            class_name="radar-hud-label radar-hud-bottom-right",
            spacing="1",
            align_items="end",
        ),
        class_name="glass-panel-main hub-radar-frame",
        width="100%",
        min_height="520px",
        spacing="0",
    )


def hub_page() -> rx.Component:
    """Advanced dashboard layout for the Aletheia Gate hub."""
    return rx.box(
        rx.box(class_name="hub-ambient-orb hub-ambient-a"),
        rx.box(class_name="hub-ambient-orb hub-ambient-b"),
        rx.box(class_name="hub-ambient-orb hub-ambient-c"),
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.image(src="/logo.png", width="56px", class_name="logo-glow"),
                    rx.vstack(
                        rx.heading("Aletheia Gate", size="5", class_name="neon-text-cyan"),
                        rx.text(
                            "EPISTEMIC COMMAND",
                            size="1",
                            color="#8b9ab0",
                            letter_spacing="2px",
                            class_name="font-jetbrains",
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    width="100%",
                    align_items="center",
                    spacing="3",
                ),
                rx.vstack(
                    sidebar_item("layout-dashboard", "Dashboard", "/hub", active=True),
                    sidebar_item("message-square", "Chat", "/chat"),
                    sidebar_item("bar-chart-2", "Analysis", "/analysis"),
                    sidebar_item("settings", "Settings", "/settings"),
                    sidebar_item("archive", "Archive", "/archive"),
                    width="100%",
                    spacing="2",
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text("Security Layer", size="1", color="#8aa0b4", class_name="font-jetbrains"),
                    rx.hstack(
                        rx.icon("shield-check", size=16, color="#14f1d9"),
                        rx.text("Zero-trust lock engaged", size="2", color="#d8e5ef"),
                        width="100%",
                        align_items="center",
                        spacing="2",
                    ),
                    class_name="hub-security-card",
                    width="100%",
                    spacing="1",
                ),
                rx.link(
                    rx.button("TERMINATE SESSION", class_name="logout-btn-neon", width="100%"),
                    href="/",
                    width="100%",
                ),
                class_name="hub-sidebar glass-sidebar",
                width="290px",
                min_width="260px",
                spacing="5",
            ),
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Truth Operations Hub", size="8", class_name="neon-text-cyan", font_weight="700"),
                        rx.text(
                            "High-fidelity reasoning telemetry and model integrity observability.",
                            size="3",
                            color="#b8c8d6",
                            font_weight="400",
                        ),
                        spacing="1",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.vstack(
                        rx.hstack(
                            rx.icon("activity", color="#00FF9C", size=16),
                            rx.text(
                                f"CORE STATUS: {HubState.system_status}",
                                color="#00FF9C",
                                class_name="font-jetbrains",
                                size="2",
                            ),
                            class_name="hub-status-pill",
                            spacing="2",
                            align_items="center",
                        ),
                        rx.text("refresh: 250ms", size="1", color="#7f97ab", class_name="font-jetbrains"),
                        spacing="1",
                        align_items="end",
                    ),
                    width="100%",
                    align_items="center",
                    class_name="hub-top-row",
                ),
                rx.hstack(
                    rx.box(hallucination_radar(), class_name="hub-radar-card"),
                    rx.vstack(
                        stat_card("Token Throughput", HubState.throughput, "live", "teal"),
                        stat_card("Inference Latency", HubState.latency, "stable", "blue"),
                        stat_card("Anomaly Rate", HubState.anomaly_rate, "low", "green"),
                        rx.vstack(
                            rx.hstack(
                                rx.icon("cpu", color="#00e5ff", size=19),
                                rx.heading("AI Analysis Panel", size="5", color="#0cf9ff", class_name="font-orbitron", font_weight="700"),
                                spacing="2",
                                align_items="center",
                                width="100%",
                            ),
                            rx.text("Active data stream", color="#8b9ab0", size="2"),
                            rx.box(
                                rx.text(
                                    "> " + HubState.current_query,
                                    size="2",
                                    color="#d9fff4",
                                    class_name="font-jetbrains",
                                ),
                                class_name="hub-stream-box",
                                width="100%",
                            ),
                            rx.vstack(
                                model_row("GPT-4o", HubState.gpt_score, "Secure", "green"),
                                model_row("Llama-3", HubState.llama_score, "Review", "amber"),
                                model_row("Groq-70B", HubState.groq_score, "Observe", "orange"),
                                width="100%",
                                spacing="4",
                            ),
                            class_name="hub-panel glass-card",
                            width="100%",
                            spacing="4",
                            align_items="start",
                        ),
                        spacing="4",
                        class_name="hub-stat-column",
                    ),
                    class_name="hub-hero-grid",
                    width="100%",
                    align_items="stretch",
                ),
                class_name="hub-main",
                width="100%",
                spacing="5",
            ),
            class_name="hub-layout",
            spacing="0",
            width="100%",
        ),
        class_name="main-bg-dark hub-shell",
        width="100%",
    )