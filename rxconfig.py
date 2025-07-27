import reflex as rx

config = rx.Config(
    app_name="four_consonants_in_a_row",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)