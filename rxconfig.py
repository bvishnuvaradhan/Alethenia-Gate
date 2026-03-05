import reflex as rx

config = rx.Config(
    app_name="aletheia_gate",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)