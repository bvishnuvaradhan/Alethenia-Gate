import reflex as rx
from .pages.entry import entry_page
from .pages.hub import hub_page
from .pages.insight import insight_page
from .pages.vault import vault_page
from .pages.login import login_page
from .pages.signup import signup_page

app = rx.App(
    theme=rx.theme(
        appearance="dark", 
        accent_color="blue", 
        radius="large"
    ),
    # Link your custom CSS for the advanced animations
    stylesheets=["/styles.css", "/hub_styles.css"], 
)

# This sets entry_page as the home route (localhost:3000/)
app.add_page(entry_page, route="/")
app.add_page(hub_page, route="/hub")
app.add_page(insight_page, route="/insight")
app.add_page(vault_page, route="/vault")
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")