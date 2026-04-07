"""Analysis state — aggregates historical query results into chart-ready data."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

import reflex as rx

from .base import State
from ..backend.mongodb_store import get_query_results


class AnalysisState(State):
    analysis_loading: bool = False
    analysis_error: str = ""

    total_queries: int = 0
    avg_truth: int = 0
    avg_web_score: int = 0
    avg_latency: int = 0
    top_source: str = "N/A"
    top_model: str = "N/A"

    trend_data: list[dict[str, Any]] = []
    model_average_data: list[dict[str, Any]] = []
    web_source_breakdown: list[dict[str, Any]] = []
    risk_breakdown: list[dict[str, Any]] = []
    latency_trend_data: list[dict[str, Any]] = []

    def _provider_bucket(self, model_name: str) -> str:
        name = (model_name or "").lower()
        if "groq" in name or "llama" in name:
            return "groq"
        if "gemini" in name or "google" in name:
            return "gemini"
        if "cohere" in name or "command-r" in name:
            return "cohere"
        if "anthropic" in name or "claude" in name:
            return "anthropic"
        if "openai" in name or "gpt" in name:
            return "openai"
        return "other"

    def _normalize_source(self, source_name: str) -> str:
        src = (source_name or "").strip()
        low = src.lower()
        if "wikipedia" in low:
            return "Wikipedia"
        if "duckduckgo" in low:
            return "DuckDuckGo"
        if "wikidata" in low:
            return "Wikidata"
        if "openalex" in low:
            return "OpenAlex"
        if "pubmed" in low or "entrez" in low:
            return "PubMed"
        if "arxiv" in low:
            return "arXiv"
        if "google" in low:
            return "Google Search"
        return src.split(":", 1)[0].strip() if ":" in src else (src or "Unknown")

    async def load_analysis(self):
        self.analysis_loading = True
        self.analysis_error = ""
        yield

        username = (self.username or "").strip() or "anonymous"
        results = await get_query_results(username, limit=250)
        if not results and username != "anonymous":
            results = await get_query_results("anonymous", limit=250)

        if not results:
            self.analysis_loading = False
            self.analysis_error = "No interrogation data found yet. Run a few queries first."
            self.total_queries = 0
            self.trend_data = []
            self.model_average_data = []
            self.web_source_breakdown = []
            self.risk_breakdown = []
            self.latency_trend_data = []
            yield
            return

        ordered = list(reversed(results))  # oldest -> newest for timeline charts

        provider_scores: dict[str, list[float]] = defaultdict(list)
        source_counter: Counter[str] = Counter()
        risk_counter: Counter[str] = Counter()
        model_name_scores: dict[str, list[float]] = defaultdict(list)

        trend_rows: list[dict[str, Any]] = []
        latency_rows: list[dict[str, Any]] = []

        total_truth = 0.0
        total_web = 0.0
        total_latency = 0.0

        for idx, result in enumerate(ordered):
            truth = int(result.get("truth_score", 0) or 0)
            web_score_raw = float(result.get("web_score", 0.0) or 0.0)
            web_pct = int(web_score_raw * 100) if web_score_raw <= 1.0 else int(web_score_raw)
            latency = int(result.get("latency_total", 0) or 0)

            total_truth += truth
            total_web += web_pct
            total_latency += latency

            if truth >= 70:
                risk_counter["LOW"] += 1
            elif truth >= 40:
                risk_counter["MEDIUM"] += 1
            else:
                risk_counter["HIGH"] += 1

            per_query_provider: dict[str, list[float]] = defaultdict(list)
            for m in result.get("models", []):
                model_name = str(m.get("name", "Unknown") or "Unknown")
                try:
                    score = float(m.get("score", 0.0) or 0.0)
                except Exception:
                    score = 0.0

                model_name_scores[model_name].append(score)
                bucket = self._provider_bucket(model_name)
                if bucket != "other":
                    per_query_provider[bucket].append(score)
                    provider_scores[bucket].append(score)

            trend_rows.append(
                {
                    "query": f"Q{idx + 1}",
                    "overall": truth,
                    "groq": round(sum(per_query_provider["groq"]) / len(per_query_provider["groq"]), 1)
                    if per_query_provider["groq"] else None,
                    "gemini": round(sum(per_query_provider["gemini"]) / len(per_query_provider["gemini"]), 1)
                    if per_query_provider["gemini"] else None,
                    "cohere": round(sum(per_query_provider["cohere"]) / len(per_query_provider["cohere"]), 1)
                    if per_query_provider["cohere"] else None,
                    "anthropic": round(sum(per_query_provider["anthropic"]) / len(per_query_provider["anthropic"]), 1)
                    if per_query_provider["anthropic"] else None,
                    "openai": round(sum(per_query_provider["openai"]) / len(per_query_provider["openai"]), 1)
                    if per_query_provider["openai"] else None,
                }
            )

            latency_rows.append({"query": f"Q{idx + 1}", "latency": latency})

            for src in result.get("web_source_names", []) or []:
                source_counter[self._normalize_source(str(src))] += 1

        model_avg_rows: list[dict[str, Any]] = []
        for name, vals in model_name_scores.items():
            if not vals:
                continue
            model_avg_rows.append({"model": name[:24], "score": round(sum(vals) / len(vals), 1)})
        model_avg_rows.sort(key=lambda x: x["score"], reverse=True)

        colors = ["#00e5a0", "#00cfff", "#ffaa00", "#bf5fff", "#ff0080", "#58a6ff", "#39ff14", "#f97316"]
        web_rows = []
        for i, (name, cnt) in enumerate(source_counter.most_common(8)):
            web_rows.append({"name": name, "count": cnt, "color": colors[i % len(colors)]})

        risk_rows = [
            {"name": "LOW", "count": risk_counter.get("LOW", 0), "color": "#00e5a0"},
            {"name": "MEDIUM", "count": risk_counter.get("MEDIUM", 0), "color": "#ffaa00"},
            {"name": "HIGH", "count": risk_counter.get("HIGH", 0), "color": "#ff0080"},
        ]

        top_model = model_avg_rows[0]["model"] if model_avg_rows else "N/A"
        top_source = web_rows[0]["name"] if web_rows else "N/A"

        n = len(ordered)
        self.total_queries = n
        self.avg_truth = int(total_truth / n) if n else 0
        self.avg_web_score = int(total_web / n) if n else 0
        self.avg_latency = int(total_latency / n) if n else 0
        self.top_source = top_source
        self.top_model = top_model

        self.trend_data = trend_rows
        self.model_average_data = model_avg_rows[:8]
        self.web_source_breakdown = web_rows
        self.risk_breakdown = risk_rows
        self.latency_trend_data = latency_rows

        # Keep sidebar score aligned with aggregate dashboard/analysis score.
        self.truth_score = self.avg_truth

        self.analysis_loading = False
        yield