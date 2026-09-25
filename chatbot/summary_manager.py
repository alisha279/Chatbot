import json
from pathlib import Path


class SummaryManager:

    def __init__(self):

        self.file_path = Path("data/summary.json")
        self.summary = ""

        self.load_summary()

    # ---------------------------------

    def get_summary(self):
        return self.summary

    # ---------------------------------

    def update_summary(self, summary):

        self.summary = summary
        self.save_summary()

    # ---------------------------------

    def clear(self):

        self.summary = ""
        self.save_summary()

    # ---------------------------------

    def load_summary(self):

        if not self.file_path.exists():
            self.save_summary()
            return

        with open(self.file_path, "r", encoding="utf-8") as file:

            data = json.load(file)

            self.summary = data.get(
                "summary",
                ""
            )

    # ---------------------------------

    def save_summary(self):

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(self.file_path, "w", encoding="utf-8") as file:

            json.dump(
                {
                    "summary": self.summary
                },
                file,
                indent=4
            )