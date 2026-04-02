"""Interrogation page — stream + segments + web verify with sources + fact check + meter."""
import reflex as rx
from ..state.base import State
from ..state.interrogation_state import IntState
from .ui import corners, glass, hud


def _styled_response() -> rx.Component:
    """Render response with styled claim highlighting for wrong words."""
    return rx.cond(
        IntState.styled_claim.length() > 0,
        rx.hstack(
            rx.foreach(
                IntState.styled_claim,
                lambda word: rx.text(
                    word["text"],
                    color=rx.cond(word["is_wrong"], "#ff4d4f", "rgba(220,185,240,.8)"),
                    text_decoration=rx.cond(word["is_wrong"], "line-through", "none"),
                    font_weight=rx.cond(word["is_wrong"], "bold", "normal"),
                    margin_right="4px",
                    style={
                        "text_shadow": rx.cond(
                            word["is_wrong"],
                            "0 0 6px #ff4d4f",
                            "none"
                        )
                    }
                )
            ),
            spacing="0",
            wrap="wrap",
            width="100%",
            class_name="ag-stxt",
        ),
        rx.text(IntState.stream, class_name="ag-stxt"),
    )


def _seg(s) -> rx.Component:
    col = rx.cond(s.status=="verified","#00e5a0",rx.cond(s.status=="flagged","#ff0080","#ffaa00"))
    lbg = rx.cond(s.status=="verified","rgba(0,229,160,.1)",rx.cond(s.status=="flagged","rgba(255,0,128,.1)","rgba(255,170,0,.1)"))
    lbd = rx.cond(s.status=="verified","1px solid rgba(0,229,160,.35)",rx.cond(s.status=="flagged","1px solid rgba(255,0,128,.35)","1px solid rgba(255,170,0,.35)"))
    bl  = rx.cond(s.status=="verified","3px solid #00e5a0",rx.cond(s.status=="flagged","3px solid #ff0080","3px solid #ffaa00"))
    ico = rx.cond(s.status=="verified","✓",rx.cond(s.status=="flagged","⚠","?"))
    pct = (s.confidence * 100).to(int).to_string() + "%"
    return rx.hstack(
        rx.box(ico, class_name="ag-segico",
               style={"color":col,"background":lbg,"border":lbd,"text_shadow":"0 0 10px currentColor"}),
        rx.vstack(
            rx.hstack(
                rx.text(s.status.upper(), class_name="ag-seglbl",
                        style={"color":col,"text_shadow":"0 0 8px currentColor"}),
                rx.text(pct, class_name="ag-segconf"),
                spacing="3", align="center",
            ),
            rx.text(s.text, class_name="ag-segtxt"),
            rx.cond(s.reason!="",
                rx.hstack(rx.text("⚠",font_size="11px",color="#ffaa00"),
                          rx.text(s.reason,class_name="ag-segr"),
                          spacing="2",align="center")),
            align="start", spacing="2",
        ),
        class_name="ag-seg", border_left=bl, spacing="3", align="start",
    )


def _fact_error(e) -> rx.Component:
    conf_pct = (e.confidence * 100).to(int).to_string() + "%"
    return rx.box(
        rx.vstack(
            rx.text("WRONG CLAIM DETECTED",
                    font_family="'Orbitron',monospace", font_size="7px",
                    letter_spacing="0.2em", color="var(--red)"),
            rx.text(e.claim, class_name="ag-fc-claim"),
            rx.text("CORRECTION",
                    font_family="'Orbitron',monospace", font_size="7px",
                    letter_spacing="0.2em", color="#00e5a0", margin_top="4px"),
            rx.text(e.correction, class_name="ag-fc-correct"),
            rx.hstack(
                rx.text("Confidence: " + conf_pct, class_name="ag-fc-conf"),
                rx.text("· " + e.source, class_name="ag-fc-conf"),
                spacing="2",
            ),
            spacing="1", align="start",
        ),
        class_name="ag-fc-error",
    )


def _source_row(src_item) -> rx.Component:
    """Single web source row showing the source name with a clickable link icon on the right."""
    return rx.hstack(
        rx.box(class_name="ag-dot ag-dot-c",
               style={"width":"5px","height":"5px","flex_shrink":"0"}),
        rx.text(src_item.name,
                font_family="'JetBrains Mono',monospace",
                font_size="10px", color="rgba(220,185,240,.65)",
                flex="1",
                style={"overflow":"hidden","white_space":"nowrap","text_overflow":"ellipsis"}),
        rx.cond(
            src_item.url != "",
            rx.link(
                rx.box("🔗",
                       font_family="'JetBrains Mono',monospace",
                       font_size="11px", color="rgba(0,245,255,.7)",
                       padding="4px 8px",
                       border_radius="3px",
                       background="rgba(0,245,255,.05)",
                       _hover={"background":"rgba(0,245,255,.15)","color":"rgba(0,245,255,1)","cursor":"pointer"},
                       transition="all 0.2s ease"),
                href=src_item.url,
                is_external=True,
                style={"text_decoration":"none"}
            ),
        ),
        spacing="2", align="center",
        padding_y="3px",
        border_bottom="1px solid rgba(0,245,255,.04)",
        width="100%",
    )


def _fact_check_panel() -> rx.Component:
    return rx.cond(
        State.fact_check_done,
        glass(
            corners(),
            rx.vstack(
                rx.hstack(
                    rx.text("🔍", font_size="14px"),
                    rx.text("FACT CHECK RESULTS", class_name="ag-fc-title"),
                    rx.spacer(),
                    rx.cond(
                        State.fact_checker_used != "",
                        rx.text("via " + State.fact_checker_used, class_name="ag-fc-checker"),
                    ),
                    spacing="2", align="center",
                ),
                rx.cond(
                    State.has_errors,
                    rx.hstack(
                        rx.text("⚠", font_size="14px", color="var(--red)"),
                        rx.text(
                            State.fact_errors.length().to_string() + " factual error(s) detected — score penalised by " +
                            (State.fact_penalty * 100).to(int).to_string() + "%",
                            class_name="ag-fc-penalty",
                        ),
                        spacing="2", align="center",
                        padding="8px 14px",
                        background="rgba(255,51,85,.06)",
                        border="1px solid rgba(255,51,85,.2)",
                        border_radius="4px",
                    ),
                    rx.text("✓ No factual errors detected.", class_name="ag-fc-ok"),
                ),
                rx.cond(
                    State.has_errors,
                    rx.vstack(rx.foreach(State.fact_errors, _fact_error),
                              spacing="2", width="100%"),
                ),
                spacing="3", width="100%",
            ),
            class_name="ag-fc-panel",
            width="100%",
        ),
    )


def _web_panel() -> rx.Component:
    return rx.cond(
        State.web_sources > 0,
        glass(
            corners(),
            rx.vstack(
                # Header
                rx.hstack(
                    rx.box(class_name="ag-dot ag-dot-c"),
                    rx.text("WEB VERIFICATION", class_name="ag-web-title"),
                    rx.spacer(),
                    rx.text(
                        State.web_sources.to_string() + " source(s)",
                        font_family="'JetBrains Mono',monospace",
                        font_size="10px", color="rgba(220,185,240,.5)",
                    ),
                    spacing="2", align="center",
                ),

                # Web score bar
                rx.hstack(
                    rx.text("WEB SCORE", class_name="ag-web-score-lbl"),
                    rx.text(State.web_score_pct, class_name="ag-web-score-val"),
                    rx.box(
                        rx.box(class_name="ag-web-bar-fill", width=State.web_score_pct),
                        class_name="ag-web-bar",
                    ),
                    class_name="ag-web-score-row", width="100%",
                ),

                # Source names and URLs — show exactly which sites were checked
                rx.cond(
                    State.web_source_names.length() > 0,
                    rx.vstack(
                        rx.text("SOURCES CHECKED",
                                font_family="'Orbitron',monospace",
                                font_size="7px", letter_spacing="0.2em",
                                color="rgba(220,185,240,.4)", margin_bottom="4px"),
                        rx.foreach(State.web_sources_combined, _source_row),
                        spacing="0", width="100%", margin_bottom="8px",
                    ),
                ),

                # Summary
                rx.text(State.web_summary, class_name="ag-web-summary"),

                # Verified facts
                rx.cond(
                    State.facts_verified.length() > 0,
                    rx.vstack(
                        rx.text("✓ CONFIRMED BY WEB",
                                font_family="'Orbitron',monospace",
                                font_size="7px", letter_spacing="0.2em",
                                color="#00e5a0",
                                style={"text_shadow":"0 0 6px rgba(0,229,160,.5)"}),
                        rx.foreach(State.facts_verified,
                            lambda f: rx.hstack(
                                rx.text("✓", class_name="ag-fact-ico", color="#00e5a0"),
                                rx.text(f, class_name="ag-fact-txt"),
                                class_name="ag-fact-row",
                            )),
                        spacing="2", width="100%", align="start",
                    ),
                ),

                # Unverified
                rx.cond(
                    State.facts_unverified.length() > 0,
                    rx.vstack(
                        rx.text("⚠ NOT MATCHED IN WEB SOURCES",
                                font_family="'Orbitron',monospace",
                                font_size="7px", letter_spacing="0.2em",
                                color="#ffaa00",
                                style={"text_shadow":"0 0 6px rgba(255,170,0,.5)"},
                                margin_top="8px"),
                        rx.foreach(State.facts_unverified,
                            lambda f: rx.hstack(
                                rx.text("?", class_name="ag-fact-ico", color="#ffaa00"),
                                rx.text(f, class_name="ag-fact-txt"),
                                class_name="ag-fact-row",
                            )),
                        spacing="2", width="100%", align="start",
                    ),
                ),

                spacing="3", width="100%",
            ),
            class_name="ag-web-panel",
            width="100%",
        ),
    )


def _api_response_card(m) -> rx.Component:
    return rx.cond(
        (m.available == True) & (m.response != "") & (m.is_mock == False),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(m.name,
                            font_family="'Orbitron',monospace",
                            font_size="9px",
                            letter_spacing="0.12em",
                            color="rgba(0,245,255,.9)"),
                    rx.spacer(),
                    rx.text((m.latency).to_string() + "ms",
                            font_family="'JetBrains Mono',monospace",
                            font_size="9px",
                            color="rgba(220,185,240,.5)"),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    m.response,
                    font_family="'JetBrains Mono',monospace",
                    font_size="11px",
                    color="rgba(220,235,245,.86)",
                    line_height="1.55",
                    style={"white_space": "pre-wrap"},
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            padding="10px",
            border="1px solid rgba(0,245,255,.16)",
            border_radius="8px",
            background="rgba(8,14,22,.55)",
            width="100%",
        ),
    )


def _api_responses_panel() -> rx.Component:
    return rx.cond(
        State.models.length() > 0,
        glass(
            corners(),
            rx.vstack(
                rx.hstack(
                    rx.box(class_name="ag-dot ag-dot-c"),
                    rx.text("API RESPONSES", class_name="ag-web-title"),
                    rx.spacer(),
                    rx.text(
                        "available model outputs",
                        font_family="'JetBrains Mono',monospace",
                        font_size="10px",
                        color="rgba(220,185,240,.5)",
                    ),
                    spacing="2", align="center",
                ),
                rx.vstack(
                    rx.foreach(State.models, _api_response_card),
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            width="100%",
        ),
    )


def interrogation_page() -> rx.Component:
    return rx.hstack(
        rx.vstack(
            # Input
            glass(corners(), rx.vstack(
                rx.hstack(rx.box(class_name="ag-dot ag-dot-p"),
                          hud("SUBMIT QUERY TO TRUTH ENGINE","ag-h-p"),
                          spacing="2",align="center"),
                rx.hstack(
                    rx.text_area(
                        placeholder="Enter your prompt for forensic analysis...",
                        value=IntState.prompt,
                        on_change=IntState.set_prompt,
                        class_name="ag-textarea", width="100%",
                    ),
                    rx.box(
                        rx.cond(IntState.running,"◈  ANALYZING...","⬡  ANALYZE"),
                        class_name="ag-btn", on_click=IntState.submit,
                        cursor="pointer", align_self="flex-end", white_space="nowrap",
                    ),
                    spacing="3",align="end",width="100%",
                ),
                spacing="4",width="100%",
            ), width="100%"),

            # Terminal stream
            glass(corners(), rx.vstack(
                rx.hstack(
                    rx.hstack(rx.box(class_name="ag-tdr ag-tdr-r"),
                              rx.box(class_name="ag-tdr ag-tdr-a"),
                              rx.box(class_name="ag-tdr ag-tdr-g"),spacing="2"),
                    rx.spacer(),
                    rx.box(class_name="ag-dot",style={
                        "background":rx.cond(IntState.streaming,"#00cfff","rgba(220,185,240,.3)"),
                        "animation":rx.cond(IntState.streaming,"pulse .8s infinite","none"),
                    }),
                    hud("PRIMARY MODEL STREAM"),
                    rx.cond(IntState.streaming,rx.text("● LIVE",class_name="ag-live")),
                    spacing="2",align="center",width="100%",
                ),
                rx.box(
                    _styled_response(),
                    rx.cond(IntState.streaming,rx.text("▌",class_name="ag-cur")),
                    class_name="ag-sbox",
                ),
                spacing="3",width="100%",
            ), width="100%"),

            # Segments
            rx.cond(
                State.segments.length() > 0,
                glass(corners(), rx.vstack(
                    rx.hstack(
                        hud("FORENSIC SEGMENT ANALYSIS"),
                        rx.spacer(),
                        rx.text(State.segments.length().to_string()+" segments",
                                font_family="'JetBrains Mono',monospace",
                                font_size="10px",color="rgba(220,185,240,.38)"),
                    ),
                    rx.foreach(State.segments, _seg),
                    spacing="4",width="100%",
                ), width="100%"),
            ),

            # Web verification panel
            _web_panel(),

            # Fact check
            _fact_check_panel(),

            # Per-API responses
            _api_responses_panel(),

            # Error
            rx.cond(
                State.err_msg != "",
                rx.box(rx.hstack(
                    rx.text("⚠",font_size="16px",color="var(--red)"),
                    rx.text(State.err_msg,font_family="'JetBrains Mono',monospace",
                            font_size="12px",color="var(--red)"),
                    spacing="2",align="center"),class_name="ag-err"),
            ),

            spacing="4", flex="1", overflow_y="auto", width="100%", min_width="0",
        ),

        # Integrity meter
        glass(corners(), rx.vstack(
            hud("SCORE"), hud("METER"),
            rx.box(
                rx.box(class_name="ag-mtick",bottom="75%"),
                rx.box(class_name="ag-mtick",bottom="50%"),
                rx.box(class_name="ag-mtick",bottom="25%"),
                rx.box(class_name="ag-mbfill",height=State.truth_score.to_string()+"%",
                    style={"background":rx.cond(State.truth_score>=70,
                               "linear-gradient(to top,#00e5a0,rgba(0,229,160,.3))",
                               rx.cond(State.truth_score>=40,
                               "linear-gradient(to top,#ffaa00,rgba(255,170,0,.3))",
                               "linear-gradient(to top,#ff0080,rgba(255,0,128,.3))")),
                           "box_shadow":rx.cond(State.truth_score>=70,"0 0 15px #00e5a0",
                               rx.cond(State.truth_score>=40,"0 0 15px #ffaa00","0 0 15px #ff0080"))}),
                class_name="ag-mbwrap",
            ),
            rx.text(State.truth_score, class_name="ag-mscore",
                    style={"color":State.score_color,"text_shadow":"0 0 25px currentColor"}),
            rx.text(State.risk_label, class_name="ag-mrisk",
                    style={"color":State.score_color,"text_shadow":"0 0 10px currentColor"}),
            rx.text(State.segments.length().to_string()+" segs", class_name="ag-msegs"),
            rx.cond(State.fact_check_done,
                rx.cond(
                    State.has_errors,
                    rx.vstack(
                        rx.box(height="1px",width="100%",
                               background="linear-gradient(90deg,transparent,rgba(255,51,85,.3),transparent)",
                               margin_y="4px"),
                        hud("FACT CHK"),
                        rx.vstack(
                            rx.text(State.fact_errors.length().to_string()+" ERR",
                                    font_family="'Orbitron',monospace",font_size="14px",
                                    font_weight="900",color="var(--red)",
                                    style={"text_shadow":"0 0 12px rgba(255,51,85,.6)"}),
                            rx.text("-"+(State.fact_penalty*100).to(int).to_string()+"%",
                                    font_family="'Orbitron',monospace",font_size="10px",color="var(--red)"),
                            align="center",spacing="0",
                        ),
                        align="center",spacing="1",
                    ),
                ),
            ),
            align="center", spacing="3", width="100%",
        ), class_name="ag-meter", width="125px", flex_shrink="0", min_height="550px"),

        spacing="4", align="stretch", width="100%", class_name="ag-intpg",
    )
