# state.py
# import asyncio
import os
import reflex as rx
from langchain_community.llms import Ollama
from pyriodic_table.periodictable import PeriodicTable
from pyriodic_table import chemelements

# OLLAMA_MODEL = "llama3.2:3b"
# OLLAMA_MODEL = "qwen3:1.7b"
# OLLAMA_MODEL = "gemma3:1b"

# OLLAMA_MODEL = "everythinglm:13b"
# OLLAMA_MODEL = "dolphin-mixtral:8x7b"
# OLLAMA_MODEL = "gemma2:latest"
# OLLAMA_MODEL = "gemma3:12b"
# OLLAMA_MODEL = "dolphin-phi:latest"
# OLLAMA_MODEL = "phi4:latest"
OLLAMA_MODEL = "qwen2.5:14b"


class State(rx.State):

    # The current question being asked.
    question: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str, list[dict[str, str]]]] = []
    elements_in_response: str

    def compute_elements_in_response(self, answer):
        """Compute the elements in the response."""
        for element in answer.split("-"):
            el_obj = PeriodicTable().get_element_by_symbol(str(element))
            self.elements_in_response += f"{el_obj.atomic_number}:{el_obj.symbol}-"
        self.elements_in_response = self.elements_in_response.rstrip("-")

    @rx.event
    async def answer(self):
        # Our chatbot has some brains now!
        _system_prompt = "You are a helpful assistant that takes in a words and tries to find its representation in terms of elements of the periodic table."
        _system_prompt += 'For example, the word "hello" can be represented as "He-Li-O", where "He" is Helium, "Li" is Lithium, and "O" is Oxygen. "Science" can be represented as "Si-Ce-N-Ce", where "Si" is Silicon, "Ce" is Cerium, and "N" is Nitrogen.'
        _system_prompt += f'For reference, here is the periodic table of elements: {[_p.symbol for _p in PeriodicTable().elements]}'
        _system_prompt += 'DO NOT make up any elements.'
        _system_prompt += "Output JUST the elements in the periodic table that represent the word, separated by hyphens. DO NOT INCLUDE ANY OTHER TEXT OR EXPLANATION."
        context = [{"role": "system", "content": _system_prompt}] + \
            [{"role": "user", "content": self.question}]

        agent = Ollama(model=OLLAMA_MODEL,base_url=os.getenv('OLLAMA_BASE_URL'),)

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((
             self.question, answer, [{
                        'atomic_number': '1',
                        'symbol': 'H',
                    }],))

        # Clear the question input.
        self.question = ""
        # Yield here to clear the frontend input before continuing.
        yield

        # for chunk in agent.stream(context):
        #     print(chunk, end="", flush=True)
        #     response += chunk
        
        for chunk in agent.stream(context):
            # if hasattr(item.choices[0].delta, "content"):
            #     if item.choices[0].delta.content is None:
            #         # presence of 'None' indicates the end of the response
            #         break
                answer += chunk
                # print(self.chat_history)
                self.chat_history[-1] = (
                    self.chat_history[-1][0],
                    answer,
                    [{
                        'atomic_number': '1',
                        'symbol': 'H',
                    }],
                )
                yield
        self.compute_elements_in_response(answer)
        self.chat_history[-1] = (
            self.chat_history[-1][0],
            answer,
            [{
                'atomic_number': '1',
                'symbol': 'H',
            }],
        )
        