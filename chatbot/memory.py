import json
from pathlib import Path


class ConversationMemory:

    def __init__(self):

        self.file_path = Path("data/chats.json")
        self.history = []

        self.load_history()

    # -------------------------------------------------

    def add_user_message(self, message):

        self.history.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": message
                    }
                ]
            }
        )

        self.save_history()

    # -------------------------------------------------

    def add_bot_message(self, message):

        self.history.append(
            {
                "role": "model",
                "parts": [
                    {
                        "text": message
                    }
                ]
            }
        )

        self.save_history()

    # -------------------------------------------------

    def get_history(self):
        return self.history

    # -------------------------------------------------

    def get_recent_messages(self, count):

        return self.history[-count:]

    # -------------------------------------------------

    def trim_history(self, keep_recent):

        if keep_recent <= 0:
            self.history = []

        else:
            self.history = self.get_recent_messages(
                keep_recent
            )

        self.save_history()

    # -------------------------------------------------

    def clear(self):

        self.history = []

        self.save_history()

    # -------------------------------------------------

    def load_history(self):

        if not self.file_path.exists():
            self.history = []
            return

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                self.history = json.load(file)

        except Exception:

            self.history = []

    # -------------------------------------------------

    def save_history(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.history,
                file,
                indent=4,
                ensure_ascii=False
            )