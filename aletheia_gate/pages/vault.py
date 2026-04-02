"""Vault page — fixed layout, full width, auto-loads entries."""
import reflex as rx
from ..state.vault_state import VaultState
from .ui import corners, glass, hud


def _row(e) -> rx.Component:
    sc  = rx.cond(e.truth_score >= 70, "#00e5a0",
          rx.cond(e.truth_score >= 40, "#ffaa00", "#ff0080"))
    risk= rx.cond(e.truth_score >= 70, "LOW",
          rx.cond(e.truth_score >= 40, "MED", "HIGH"))
    rbg = rx.cond(e.truth_score >= 70, "rgba(0,229,160,.12)",
          rx.cond(e.truth_score >= 40, "rgba(255,170,0,.12)", "rgba(255,0,128,.12)"))
    rbd = rx.cond(e.truth_score >= 70, "1px solid rgba(0,229,160,.25)",
          rx.cond(e.truth_score >= 40, "1px solid rgba(255,170,0,.25)",
                                       "1px solid rgba(255,0,128,.25)"))
    return rx.hstack(
        rx.text(e.custody_id, class_name="ag-vid",   flex_shrink="0", width="160px"),
        rx.text(e.prompt,     class_name="ag-vq",    flex="1",
                min_width="0", overflow="hidden", white_space="nowrap", text_overflow="ellipsis"),
        rx.hstack(
            rx.box(class_name="ag-dot",
                   style={"background": sc, "box_shadow": "0 0 8px currentColor"}),
            rx.text(e.truth_score, class_name="ag-vscore",
                    style={"color": sc, "text_shadow": "0 0 10px currentColor"}),
            spacing="2", align="center", flex_shrink="0", width="56px",
        ),
        rx.box(
            risk,
            class_name="ag-rbadge",
            flex_shrink="0",
            style={"color": sc, "background": rbg, "border": rbd, "text_shadow": "0 0 8px currentColor"},
        ),
        class_name="ag-vrow",
        align="center",
        spacing="4",
        width="100%",
    )


def vault_page() -> rx.Component:
    return rx.vstack(
        # ── Header: Title + Search/Buttons ────────────────────────────────────
        rx.vstack(
            # Title section
            rx.vstack(
                hud("SYSTEM // ARCHIVE", "ag-h-p", font_size="9px", letter_spacing="0.3em"),
                rx.text(
                    "THE VAULT",
                    font_family="'Orbitron',monospace",
                    font_size="26px", font_weight="900",
                    style={"text_shadow": "0 0 20px rgba(0,207,255,.15)"},
                ),
                rx.text(
                    "Immutable forensic record of all interrogation sessions.",
                    font_family="'JetBrains Mono',monospace",
                    font_size="10px", color="rgba(220,185,240,.42)",
                ),
                spacing="2", align="start", width="100%",
            ),
            # Search/buttons section
            rx.hstack(
                rx.input(
                    placeholder="Search...",
                    value=VaultState.vault_search,
                    on_change=VaultState.set_search,
                    class_name="ag-input",
                    flex="1",
                    min_width="0",
                ),
                rx.box(
                    "SEARCH",
                    class_name="ag-btn ag-btn-sm",
                    on_click=VaultState.search,
                    cursor="pointer",
                    flex_shrink="0",
                ),
                rx.box(
                    "↻ REFRESH",
                    class_name="ag-btn ag-btn-sm",
                    on_click=VaultState.load,
                    cursor="pointer",
                    flex_shrink="0",
                ),
                spacing="3", align="center", width="100%",
            ),
            spacing="4", width="100%", align="start",
        ),

        # ── Table ─────────────────────────────────────────────────────────────
        glass(
            corners(),
            rx.vstack(
                # Column headers
                rx.hstack(
                    rx.text("CUSTODY ID", class_name="ag-vcol", flex_shrink="0", width="160px"),
                    rx.text("QUERY",      class_name="ag-vcol", flex="1"),
                    rx.text("SCORE",      class_name="ag-vcol", flex_shrink="0", width="56px"),
                    rx.text("RISK",       class_name="ag-vcol", flex_shrink="0", width="60px"),
                    class_name="ag-vth", width="100%",
                ),
                # Rows
                rx.cond(
                    VaultState.vault_loading,
                    rx.center(
                        rx.vstack(
                            rx.box(
                                rx.box(class_name="ag-sr ag-sr1"),
                                rx.box(class_name="ag-sr ag-sr2"),
                                class_name="ag-spin", width="40px", height="40px",
                            ),
                            rx.text(
                                "Loading vault...",
                                font_family="'JetBrains Mono',monospace",
                                font_size="12px", color="#00cfff",
                                style={"animation": "pulse 1s infinite",
                                       "text_shadow": "0 0 8px rgba(0,207,255,.5)"},
                            ),
                            align="center", spacing="3",
                        ),
                        padding="50px",
                    ),
                    rx.cond(
                        VaultState.vault_log.length() > 0,
                        rx.vstack(
                            rx.foreach(VaultState.vault_log, _row),
                            spacing="0", width="100%",
                        ),
                        rx.center(
                            rx.vstack(
                                rx.text("⬢", class_name="ag-empty-i"),
                                rx.text(
                                    "No entries yet.",
                                    class_name="ag-empty-t",
                                ),
                                rx.text(
                                    "Run an interrogation then come back here.",
                                    class_name="ag-empty-t",
                                    style={"opacity": "0.55", "font_size": "11px"},
                                ),
                                align="center", spacing="2",
                            ),
                            padding="70px",
                        ),
                    ),
                ),
                spacing="0", width="100%",
            ),
            padding="0",
            overflow_x="hidden",
            overflow_y="auto",
            max_height="80vh",
            width="100%",
            class_name="ag-vtbl",
        ),

        spacing="5", width="100%", class_name="ag-vltpg", overflow="hidden",
    )
