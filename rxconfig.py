import reflex as rx
from reflex.plugins import SitemapPlugin

config = rx.Config(
    app_name="aletheia_gate",
    disable_plugins=[SitemapPlugin],
    head_components=[],
)
