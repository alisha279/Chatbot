from chatbot.prompts import (
    DEFAULT_PROMPT,
    PYTHON_PROMPT,
    DATABASE_PROMPT,
)


class PromptManager:

    def __init__(self):

        self.current_mode = "default"

        self.available_prompts = {
            "default": DEFAULT_PROMPT,
            "python": PYTHON_PROMPT,
            "database": DATABASE_PROMPT,
        }

    def get_prompt(self):
        return self.available_prompts[self.current_mode]

    def get_mode(self):
        return self.current_mode

    def set_mode(self, mode):

        if mode in self.available_prompts:
            self.current_mode = mode
            return True

        return False
    def get_available_modes(self):
        return list(self.available_prompts.keys())