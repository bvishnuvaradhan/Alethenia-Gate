"""Aletheia Gate — main entry point. Pure Reflex, one route."""
import reflex as rx
from dotenv import load_dotenv

load_dotenv()

from .styles import GLOBAL_CSS, BG, BODY
from .state.base import State
from .state.interrogation_state import IntState
from .state.vault_state import VaultState
from .state.engine_state import EngineState
from .state.analysis_state import AnalysisState
from .state.terminate_state import TermState

from .pages.landing       import landing_page
from .pages.login         import login_page
from .pages.signup        import signup_page
from .pages.layout        import shell
from .pages.dashboard     import dashboard_page
from .pages.interrogation import interrogation_page
from .pages.vault         import vault_page
from .pages.engine        import engine_page
from .pages.analysis      import analysis_page
from .pages.terminate     import terminate_page


def _chrome(content: rx.Component) -> rx.Component:
    return rx.fragment(
        rx.el.style(GLOBAL_CSS),
        rx.box(class_name="ag-grid-bg"),
        content,
    )


@rx.page(route="/", title="ALETHEIA GATE — Forensic AI Audit Suite")
def index() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(dashboard_page()), landing_page())
    )


@rx.page(route="/login", title="Login — Aletheia Gate")
def login_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(dashboard_page()), login_page())
    )


@rx.page(route="/signup", title="Signup — Aletheia Gate")
def signup_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(dashboard_page()), signup_page())
    )


@rx.page(route="/hub", title="Hub — Aletheia Gate")
def hub_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(dashboard_page()), login_page())
    )


@rx.page(route="/interrogate", title="Interrogation — Aletheia Gate")
def interrogate_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(interrogation_page()), login_page())
    )


@rx.page(route="/vault", title="Vault — Aletheia Gate", on_load=VaultState.load)
def vault_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(vault_page()), login_page())
    )


@rx.page(route="/engine", title="Engine — Aletheia Gate")
def engine_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(engine_page()), login_page())
    )


@rx.page(route="/analysis", title="Analysis — Aletheia Gate", on_load=AnalysisState.load_analysis)
def analysis_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(analysis_page()), login_page())
    )


@rx.page(route="/terminate", title="Terminate — Aletheia Gate")
def terminate_route() -> rx.Component:
    return _chrome(
        rx.cond(State.authenticated, shell(terminate_page()), login_page())
    )


app = rx.App(
    style={"background": BG, "font_family": BODY},
    # suppressHydrationWarning stops browser extension attribute mismatches
    # (Grammarly, LastPass etc inject data-* attrs into <body> before React loads)
    html_lang="en",
    html_custom_attrs={"suppress_hydration_warning": True},
    head_components=[
        rx.el.meta(name="viewport", content="width=device-width, initial-scale=1"),
        # Tell Grammarly and similar extensions to ignore this app
        rx.el.meta(name="grammarly-disable", content="true"),
        rx.el.link(rel="icon", href="/favicon.ico", type="image/x-icon"),
    ],
)
