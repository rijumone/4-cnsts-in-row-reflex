# chatapp.py
import reflex as rx
from pyriodic_table.periodictable import PeriodicTable
from loguru import logger
import json
from four_consonants_in_a_row import style
from four_consonants_in_a_row.state import State

def gen_card(element: str) -> rx.Component:
    # logger.info(f"Generating card for element: {element}")
    # print(el_obj)
    # el_obj = json.loads(element)
    return rx.card(
        # rx.text(el_obj['symbol']),
        rx.text(element),
        # rx.text(el_obj['atomic_number']),
        rx.text(element),
        size="4",
        # style=style.answer_style,
        text_align="center",
    )

def qa(question: str, answer: str, elements_in_response: list[str]) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        # rx.box(
        #     rx.text(answer, style=style.answer_style),
        #     rx.card(answer, size="4"),
        #     text_align="left",
        # ),
        rx.flex(
            rx.foreach(
                # answer.split("-"),
                elements_in_response,
                lambda element: gen_card(element),
                # lambda element: rx.card(element, size="4"),

            ),
            align_items="flex-start",
            spacing="2",
        ),
        margin_y="1em",
        width="100%",

    )



def chat() -> rx.Component:
    logger.debug(f"Chat history: {State.chat_history}")
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1], messages[2]),
        )
    )

def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=State.question,
            placeholder="Ask a question",
            on_change=State.set_question,
            style=style.input_style,
        ),
        rx.button(
            "Ask",
            on_click=State.answer,
            style=style.button_style,
        ),
    )


def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat(),
            action_bar(),
            # align="center",
        )
    )


app = rx.App()
app.add_page(index)
