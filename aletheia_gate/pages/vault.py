"""Vault page — displays all user's interrogation results from MongoDB."""
import reflex as rx
from ..state.vault_state import VaultState
from .ui import corners, glass, hud


def _detail_modal() -> rx.Component:
    """Modal popup showing full result details with facts, model responses, and web sources."""
    return rx.cond(
        VaultState.show_modal,
        rx.box(
            # Overlay
            rx.box(width="100%", height="100%", position="fixed", top="0", left="0",
                  background="rgba(0,0,0,.75)", on_click=VaultState.close_modal),
            # Modal
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.text("🔍 QUERY DETAILS", font_weight="bold", font_size="16px", color="#00cfff",
                               style={"text_shadow": "0 0 10px rgba(0,207,255,.5)"}),
                        rx.spacer(),
                        rx.box(
                            "🗑",
                            cursor="pointer",
                            width="34px",
                            height="34px",
                            display="inline-flex",
                            align_items="center",
                            justify_content="center",
                            border="1px solid rgba(255,50,80,.12)",
                            border_radius="8px",
                            background="rgba(255,50,80,.02)",
                            color="#ff3355",
                            font_size="16px",
                            on_click=lambda: VaultState.delete_result(VaultState.modal_data["custody_id"]),
                            _hover={"background": "rgba(255,50,80,.08)", "color": "#ff0000"},
                        ),
                        rx.box(
                            "✕",
                            cursor="pointer",
                            width="36px",
                            height="36px",
                            display="inline-flex",
                            align_items="center",
                            justify_content="center",
                            border="1px solid rgba(255,0,128,.08)",
                            border_radius="8px",
                            background="transparent",
                            color="#ff0080",
                            font_size="18px",
                            on_click=VaultState.close_modal,
                            _hover={"background": "rgba(255,0,128,.06)", "color": "#ff3355"},
                        ),
                        width="100%", align="center", padding_bottom="12px",
                        border_bottom="1px solid rgba(0,207,255,.4)",
                    ),
                    # Content
                    rx.vstack(
                        # Custody ID
                        rx.hstack(
                            rx.text("CUSTODY ID:", font_weight="bold", color="#00cfff", width="140px",
                                   style={"text_shadow": "0 0 6px rgba(0,207,255,.3)"}),
                            rx.text(VaultState.modal_data["custody_id"], font_family="'JetBrains Mono',monospace",
                                   font_size="12px", word_break="break-all", color="#e0d5f0"),
                            spacing="2", width="100%", align="start",
                        ),
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        # Prompt
                        rx.vstack(
                            rx.text("PROMPT:", font_weight="bold", color="#00e5a0", font_size="12px",
                                   style={"text_shadow": "0 0 6px rgba(0,229,160,.3)"}),
                            rx.box(
                                rx.text(VaultState.modal_data["prompt"], font_family="'JetBrains Mono',monospace",
                                       font_size="11px", white_space="pre-wrap", word_break="break-word", color="#e0d5f0"),
                                background="rgba(0,229,160,.05)", padding="10px", border_radius="4px",
                                border="1px solid rgba(0,229,160,.25)", width="100%", max_height="100px", overflow_y="auto",
                            ),
                            spacing="2", width="100%",
                        ),
                        # Metrics
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.hstack(
                            rx.vstack(
                                rx.text("TRUTH SCORE", font_size="9px", color="rgba(0,229,160,.9)", letter_spacing="0.1em",
                                       style={"text_shadow": "0 0 4px rgba(0,229,160,.4)"}),
                                rx.text(VaultState.modal_data["truth_score"], font_size="20px", font_weight="900",
                                       color="#00e5a0", style={"text_shadow": "0 0 12px rgba(0,229,160,.5)"}),
                                align="center",
                            ),
                            rx.vstack(
                                rx.text("CONSENSUS", font_size="9px", color="rgba(0,207,255,.9)", letter_spacing="0.1em",
                                       style={"text_shadow": "0 0 4px rgba(0,207,255,.4)"}),
                                rx.text(VaultState.modal_data["consensus_score_pct"], font_size="20px", font_weight="900",
                                       color="#00cfff", style={"text_shadow": "0 0 12px rgba(0,207,255,.5)"}),
                                align="center",
                            ),
                            rx.vstack(
                                rx.text("WEB SCORE", font_size="9px", color="rgba(255,170,0,.9)", letter_spacing="0.1em",
                                       style={"text_shadow": "0 0 4px rgba(255,170,0,.4)"}),
                                rx.text(VaultState.modal_data["web_score_pct"], font_size="20px", font_weight="900",
                                       color="#ffaa00", style={"text_shadow": "0 0 12px rgba(255,170,0,.5)"}),
                                align="center",
                            ),
                            rx.vstack(
                                rx.text("LATENCY", font_size="9px", color="rgba(191,95,255,.9)", letter_spacing="0.1em",
                                       style={"text_shadow": "0 0 4px rgba(191,95,255,.4)"}),
                                rx.text(VaultState.modal_data["latency_total"].to_string() + "ms", font_size="20px",
                                       font_weight="900", color="#bf5fff", style={"text_shadow": "0 0 12px rgba(191,95,255,.5)"}),
                                align="center",
                            ),
                            spacing="3", width="100%", justify="between",
                        ),
                        # Verified facts
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("✓ VERIFIED FACTS", font_weight="bold", color="#00e5a0", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(0,229,160,.4)"}),
                            rx.foreach(VaultState.modal_facts_verified,
                                      lambda fact: rx.box(
                                          rx.text("▪", color="#00e5a0", margin_right="8px", font_weight="bold"),
                                          rx.text(fact, font_size="12px", color="#e0d5f0", flex="1"),
                                          display="flex", align_items="flex-start", margin_bottom="6px",
                                      )),
                            spacing="1", width="100%",
                        ),
                        # Unverified facts
                        rx.vstack(
                            rx.text("✕ UNVERIFIED FACTS", font_weight="bold", color="#ff0080", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(255,0,128,.4)"}),
                            rx.foreach(VaultState.modal_facts_unverified,
                                      lambda fact: rx.box(
                                          rx.text("✕", color="#ff0080", margin_right="8px", font_weight="bold"),
                                          rx.text(fact, font_size="12px", color="#e0d5f0", flex="1"),
                                          display="flex", align_items="flex-start", margin_bottom="6px",
                                      )),
                            spacing="1", width="100%",
                        ),
                        # Final output
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("◎ PRIMARY MODEL STREAM", font_weight="bold", color="#00e5a0", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(0,229,160,.4)"}),
                            rx.box(
                                rx.text(VaultState.modal_data["final_output"],
                                       font_family="'JetBrains Mono',monospace", font_size="11px",
                                       color="#e0d5f0", white_space="pre-wrap", word_break="break-word"),
                                width="100%",
                                background="rgba(0,229,160,.05)",
                                border="1px solid rgba(0,229,160,.25)",
                                border_radius="4px",
                                padding="10px",
                                max_height="140px",
                                overflow_y="auto",
                            ),
                            spacing="2", width="100%",
                        ),
                        # Raw stream output
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("◈ RAW RESPONSE STREAM", font_weight="bold", color="#bf5fff", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(191,95,255,.4)"}),
                            rx.box(
                                rx.text(VaultState.modal_data["stream_output"],
                                       font_family="'JetBrains Mono',monospace", font_size="10px",
                                       color="#e0d5f0", white_space="pre-wrap", word_break="break-word"),
                                width="100%",
                                background="rgba(191,95,255,.05)",
                                border="1px solid rgba(191,95,255,.25)",
                                border_radius="4px",
                                padding="10px",
                                max_height="140px",
                                overflow_y="auto",
                            ),
                            spacing="2", width="100%",
                        ),
                        # Model responses
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("⚙ MODEL RESPONSES", font_weight="bold", color="#ffaa00", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(255,170,0,.4)"}),
                            rx.foreach(VaultState.modal_models,
                                      lambda model: rx.vstack(
                                          rx.hstack(
                                              rx.text(model["name"], font_weight="bold", color="#ffaa00", font_size="12px", flex="1"),
                                              rx.text(model["score"], font_weight="bold", color="#00e5a0", font_size="12px"),
                                              width="100%",
                                          ),
                                          rx.text(model["response"],
                                                 font_family="'JetBrains Mono',monospace", font_size="10px",
                                                 color="rgba(224,213,240,.7)", white_space="pre-wrap", word_break="break-word"),
                                          padding="8px", background="rgba(255,170,0,.08)", border="1px solid rgba(255,170,0,.2)",
                                          border_radius="3px", margin_bottom="6px", spacing="2",
                                      )),
                            spacing="1", width="100%",
                        ),
                        # Web sources
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("🔗 WEB SOURCES", font_weight="bold", color="#00cfff", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(0,207,255,.4)"}),
                            rx.foreach(VaultState.modal_web_sources_paired,
                                      lambda src: rx.box(
                                          rx.link(
                                              rx.text(src["name"], color="#00cfff", font_weight="bold", font_size="12px"),
                                              href=src["url"], is_external=True,
                                              _hover={"color": "#00e5a0", "text_decoration": "underline"},
                                          ),
                                          margin_bottom="6px",
                                      )),
                            spacing="1", width="100%",
                        ),
                        # Fact-check errors
                        rx.box(height="1px", width="100%", background="rgba(0,207,255,.2)"),
                        rx.vstack(
                            rx.text("⚠ FACT-CHECK ERRORS", font_weight="bold", color="#ff6b6b", font_size="12px",
                                   letter_spacing="0.1em", style={"text_shadow": "0 0 8px rgba(255,107,107,.4)"}),
                            rx.foreach(VaultState.modal_fact_errors,
                                      lambda err: rx.box(
                                          rx.vstack(
                                              rx.text(err["claim"], font_size="11px", color="#ff9d9d", font_weight="bold"),
                                              rx.text(err["correction"], font_size="10px", color="#e0d5f0"),
                                              spacing="1", width="100%",
                                          ),
                                          padding="8px",
                                          background="rgba(255,107,107,.08)",
                                          border="1px solid rgba(255,107,107,.2)",
                                          border_radius="3px",
                                          margin_bottom="6px",
                                      )),
                            spacing="1", width="100%",
                        ),
                        spacing="2", width="100%",
                    ),
                    spacing="3", width="100%", padding="16px",
                ),
                position="fixed", top="50%", left="50%", transform="translate(-50%, -50%)", z_index="1000",
                width="90%", max_width="700px", max_height="85vh", overflow_y="auto",
                background="rgba(15,20,30,.98)", border="1px solid rgba(0,207,255,.4)", border_radius="8px",
                box_shadow="0 0 60px rgba(0,207,255,.3), inset 0 0 20px rgba(0,207,255,.05)",
            ),
            position="fixed", top="0", left="0", width="100%", height="100%", z_index="999",
        ),
    )


def _row(e) -> rx.Component:
    truth_score = e["truth_score"].to(int)
    web_sources = e["web_sources"].to(int)
    segments_count = e["segments_count"].to(int)
    fact_errors_count = e["fact_errors_count"].to(int)

    sc = rx.cond(truth_score >= 70, "#00e5a0",
       rx.cond(truth_score >= 40, "#ffaa00", "#ff0080"))
    risk = rx.cond(truth_score >= 70, "LOW",
         rx.cond(truth_score >= 40, "MED", "HIGH"))
    rbg = rx.cond(truth_score >= 70, "rgba(0,229,160,.12)",
        rx.cond(truth_score >= 40, "rgba(255,170,0,.12)", "rgba(255,0,128,.12)"))
    rbd = rx.cond(truth_score >= 70, "1px solid rgba(0,229,160,.25)",
        rx.cond(truth_score >= 40, "1px solid rgba(255,170,0,.25)",
                           "1px solid rgba(255,0,128,.25)"))
    ws_txt = rx.cond(web_sources > 0, web_sources.to_string() + " src", "0 src")
    segs_txt = segments_count.to_string() + " seg"
    errs_txt = rx.cond(fact_errors_count > 0, fact_errors_count.to_string() + " err", "✓")

    return rx.hstack(
        rx.text(e["custody_id"], class_name="ag-vid",   flex_shrink="0", width="140px",
                font_family="'JetBrains Mono',monospace", font_size="9px"),
        rx.text(e["prompt"],     class_name="ag-vq",    flex="1",
                min_width="0", overflow="hidden", white_space="nowrap", text_overflow="ellipsis"),
        rx.hstack(
            rx.box(class_name="ag-dot",
                   style={"background": sc, "box_shadow": "0 0 8px currentColor"}),
            rx.text(e["truth_score"], class_name="ag-vscore",
                    style={"color": sc, "text_shadow": "0 0 10px currentColor"}),
            spacing="2", align="center", flex_shrink="0", width="50px",
        ),
        rx.hstack(
            rx.text(ws_txt, font_size="9px", color="rgba(0,207,255,.6)"),
            rx.text(segs_txt, font_size="9px", color="rgba(0,229,160,.6)"),
            rx.text(errs_txt, font_size="9px", color=rx.cond(fact_errors_count > 0, "#ff3355", "#00e5a0")),
            spacing="2", flex_shrink="0",
        ),
        rx.box(
            risk,
            class_name="ag-rbadge",
            flex_shrink="0",
            style={"color": sc, "background": rbg, "border": rbd, "text_shadow": "0 0 8px currentColor"},
        ),
        # Delete button aligned to far right
        rx.box(
            "🗑",
            cursor="pointer",
            width="36px",
            height="36px",
            display="inline-flex",
            align_items="center",
            justify_content="center",
            border="1px solid rgba(255,50,80,.08)",
            border_radius="8px",
            background="transparent",
            color="#ff3355",
            font_size="14px",
            margin_left="8px",
            on_click=lambda: VaultState.delete_result(e["custody_id"]),
            _hover={"background": "rgba(255,50,80,.06)", "color": "#ff0000"},
            flex_shrink="0",
        ),
        class_name="ag-vrow",
        align="center",
        spacing="3",
        width="100%",
        on_click=lambda: VaultState.select_result(e["custody_id"]),
        _hover={"background": "rgba(0,245,255,.05)", "cursor": "pointer"},
    )


def vault_page() -> rx.Component:
    return rx.vstack(
        # ── Header: Title + Search/Buttons ────────────────────────────────────
        rx.vstack(
            # Title section
            rx.vstack(
                rx.text(
                    "THE VAULT",
                    font_family="'Orbitron',monospace",
                    font_size="26px", font_weight="900",
                    style={"text_shadow": "0 0 20px rgba(0,207,255,.15)"},
                ),
                rx.text(
                    "All interrogation sessions for this user.",
                    font_family="'JetBrains Mono',monospace",
                    font_size="10px", color="rgba(220,185,240,.42)",
                ),
                spacing="2", align="start", width="100%",
            ),
            # Search section
            rx.hstack(
                rx.text("Search queries:", font_size="9px", color="rgba(220,185,240,.6)"),
                rx.input(
                    placeholder="Filter...",
                    value=VaultState.vault_search,
                    on_change=VaultState.set_search,
                    class_name="ag-input",
                    flex="1",
                    min_width="0",
                ),
                rx.box(
                    "↻ RELOAD",
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
                    rx.text("CUSTODY ID", class_name="ag-vcol", flex_shrink="0", width="140px", font_size="9px"),
                    rx.text("QUERY",      class_name="ag-vcol", flex="1", font_size="9px"),
                    rx.text("SCORE",      class_name="ag-vcol", flex_shrink="0", width="50px", font_size="9px"),
                    rx.text("SOURCES",    class_name="ag-vcol", flex_shrink="0", font_size="9px"),
                    rx.text("RISK",       class_name="ag-vcol", flex_shrink="0", width="70px", font_size="9px"),
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

        # Modal for detail view
        _detail_modal(),

        spacing="5", width="100%", class_name="ag-vltpg", overflow="hidden",
    )
