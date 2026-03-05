import reflex as rx

def hub_page() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading(
                    "HUB",
                    size="9",
                    weight="bold",
                    color_scheme="blue",
                ),
                rx.text(
                    "Central Hub for Aletheia Gate",
                    size="2",
                    color_scheme="gray",
                ),
                rx.link(
                    rx.button("Back to Entry"),
                    href="/",
                ),
                align="center",
                spacing="4",
            ),
            height="100vh",
        ),
        width="100%",
        height="100%",
        background="linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
    )
