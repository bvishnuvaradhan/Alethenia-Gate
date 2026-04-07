"""Analysis page — deep telemetry and trend visualization."""

import reflex as rx

from ..state.analysis_state import AnalysisState
from .ui import corners, glass, hud


def _kpi(label: str, value, color: str) -> rx.Component:
    return glass(
        corners(),
        rx.vstack(
            hud(label, font_size="9px", letter_spacing="0.08em"),
            rx.text(
                value,
                font_family="'Orbitron',monospace",
                font_size="24px",
                font_weight="900",
                style={"color": color, "text_shadow": f"0 0 16px {color}"},
            ),
            spacing="1",
            align="start",
            width="100%",
        ),
        pad="14px",
    )


def _truth_trend_chart() -> rx.Component:
    return glass(
        corners(),
        rx.vstack(
            hud("TRUTH SCORE TIMELINE"),
            rx.text(
                "Overall score vs each model provider across query history.",
                font_family="'JetBrains Mono',monospace",
                font_size="10px",
                color="rgba(220,185,240,.45)",
            ),
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="rgba(220,185,240,.16)"),
                rx.recharts.x_axis(data_key="query", stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                rx.recharts.y_axis(domain=[0, 100], stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                rx.recharts.graphing_tooltip(),
                rx.recharts.legend(),
                rx.recharts.line(type_="monotone", data_key="overall", name="Overall", stroke="#00e5a0", stroke_width=3, dot=False),
                rx.recharts.line(type_="monotone", data_key="groq", name="Groq", stroke="#00cfff", stroke_width=2, dot=False, connect_nulls=True),
                rx.recharts.line(type_="monotone", data_key="gemini", name="Gemini", stroke="#ffaa00", stroke_width=2, dot=False, connect_nulls=True),
                rx.recharts.line(type_="monotone", data_key="cohere", name="Cohere", stroke="#bf5fff", stroke_width=2, dot=False, connect_nulls=True),
                rx.recharts.line(type_="monotone", data_key="anthropic", name="Anthropic", stroke="#ff0080", stroke_width=2, dot=False, connect_nulls=True),
                rx.recharts.line(type_="monotone", data_key="openai", name="OpenAI", stroke="#58a6ff", stroke_width=2, dot=False, connect_nulls=True),
                data=AnalysisState.trend_data,
                width="100%",
                height=420,
                style={"width": "100%"},
            ),
            spacing="2",
            width="100%",
        ),
        class_name="ag-pan",
        width="100%",
    )


def _web_sources_pie() -> rx.Component:
    return glass(
        corners(),
        rx.vstack(
            hud("WEB SOURCE DISTRIBUTION"),
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    rx.foreach(
                        AnalysisState.web_source_breakdown,
                        lambda row: rx.recharts.cell(fill=row["color"]),
                    ),
                    data=AnalysisState.web_source_breakdown,
                    data_key="count",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=52,
                    outer_radius=110,
                    padding_angle=2,
                    label=True,
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.legend(),
                width="100%",
                height=340,
            ),
            spacing="2",
            width="100%",
        ),
        class_name="ag-pan",
    )


def _model_bar_chart() -> rx.Component:
    return glass(
        corners(),
        rx.vstack(
            hud("MODEL QUALITY RANKING"),
            rx.text(
                "Average truth contribution by model endpoint.",
                font_family="'JetBrains Mono',monospace",
                font_size="10px",
                color="rgba(220,185,240,.45)",
            ),
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="rgba(220,185,240,.16)"),
                rx.recharts.x_axis(data_key="model", stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                rx.recharts.y_axis(domain=[0, 100], stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(data_key="score", fill="#00cfff"),
                data=AnalysisState.model_average_data,
                width="100%",
                height=330,
            ),
            spacing="2",
            width="100%",
        ),
        class_name="ag-pan",
    )


def _latency_and_risk() -> rx.Component:
    return rx.grid(
        glass(
            corners(),
            rx.vstack(
                hud("LATENCY TREND"),
                rx.recharts.line_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke="rgba(220,185,240,.16)"),
                    rx.recharts.x_axis(data_key="query", stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                    rx.recharts.y_axis(stroke="rgba(220,185,240,.55)", tick={"fontSize": 10}),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.line(type_="monotone", data_key="latency", stroke="#bf5fff", stroke_width=2, dot=False),
                    data=AnalysisState.latency_trend_data,
                    width="100%",
                    height=280,
                ),
                spacing="2",
                width="100%",
            ),
            class_name="ag-pan",
        ),
        glass(
            corners(),
            rx.vstack(
                hud("RISK DISTRIBUTION"),
                rx.recharts.pie_chart(
                    rx.recharts.pie(
                        rx.foreach(
                            AnalysisState.risk_breakdown,
                            lambda row: rx.recharts.cell(fill=row["color"]),
                        ),
                        data=AnalysisState.risk_breakdown,
                        data_key="count",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        inner_radius=46,
                        outer_radius=98,
                        label=True,
                    ),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.legend(),
                    width="100%",
                    height=280,
                ),
                spacing="2",
                width="100%",
            ),
            class_name="ag-pan",
        ),
        columns="2",
        spacing="4",
        width="100%",
        class_name="ag-engrid",
    )


def analysis_page() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.text(
                "ANALYSIS",
                font_family="'Orbitron',monospace",
                font_size="28px",
                font_weight="900",
                style={"text_shadow": "0 0 20px rgba(0,207,255,.18)"},
            ),
            rx.text(
                "Historical audit intelligence across models, web sources, and risk signals.",
                font_family="'JetBrains Mono',monospace",
                font_size="10px",
                color="rgba(220,185,240,.45)",
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        rx.cond(
            AnalysisState.analysis_loading,
            rx.center(
                rx.vstack(
                    rx.box(
                        rx.box(class_name="ag-sr ag-sr1"),
                        rx.box(class_name="ag-sr ag-sr2"),
                        class_name="ag-spin",
                        width="40px",
                        height="40px",
                    ),
                    rx.text(
                        "Building analysis...",
                        font_family="'JetBrains Mono',monospace",
                        color="#00cfff",
                        font_size="12px",
                    ),
                    spacing="2",
                    align="center",
                ),
                width="100%",
                padding="48px",
            ),
            rx.cond(
                AnalysisState.analysis_error != "",
                glass(
                    corners(),
                    rx.text(
                        AnalysisState.analysis_error,
                        color="#ff3355",
                        font_family="'JetBrains Mono',monospace",
                        font_size="12px",
                    ),
                    class_name="ag-pan",
                ),
                rx.vstack(
                    rx.grid(
                        _kpi("TOTAL QUERIES", AnalysisState.total_queries, "#00cfff"),
                        _kpi("AVG TRUTH", AnalysisState.avg_truth.to_string() + "%", "#00e5a0"),
                        _kpi("AVG WEB SCORE", AnalysisState.avg_web_score.to_string() + "%", "#ffaa00"),
                        _kpi("AVG LATENCY", AnalysisState.avg_latency.to_string() + "ms", "#bf5fff"),
                        _kpi("TOP MODEL", AnalysisState.top_model, "#58a6ff"),
                        _kpi("TOP SOURCE", AnalysisState.top_source, "#ff0080"),
                        columns="3",
                        spacing="3",
                        width="100%",
                    ),
                    rx.box(
                        _truth_trend_chart(),
                        width="100%",
                    ),
                    rx.grid(
                        _web_sources_pie(),
                        _model_bar_chart(),
                        columns="2",
                        spacing="4",
                        width="100%",
                        class_name="ag-engrid",
                    ),
                    _latency_and_risk(),
                    spacing="4",
                    width="100%",
                ),
            ),
        ),
        spacing="4",
        align="stretch",
        width="100%",
        on_mount=AnalysisState.load_analysis,
    )
