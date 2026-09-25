import os


class DocumentLoader:

    def __init__(self, folder="knowledge"):
        self.folder = folder

    # ---------------------------------

    def load_documents(self):

        documents = []

        if not os.path.exists(self.folder):
            return documents

        for filename in os.listdir(self.folder):

            if not filename.endswith(".txt"):
                continue

            filepath = os.path.join(
                self.folder,
                filename
            )

            text = self._read_file(filepath)

            documents.append(
                {
                    "name": filename,
                    "text": text
                }
            )

        return documents

    # ---------------------------------

    def _read_file(self, filepath):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()