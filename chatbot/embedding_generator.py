from google import genai

from chatbot.config import API_KEY


class EmbeddingGenerator:
    """
    Converts text into numerical embeddings
    using Google's embedding model.
    """

    def __init__(
        self,
        model="gemini-embedding-001"
    ):

        self.model = model

        self.client = genai.Client(
            api_key=API_KEY
        )

    # --------------------------------------------------

    def generate(self, text):

        if not text:
            return []

        response = self.client.models.embed_content(
            model=self.model,
            contents=text
        )

        return response.embeddings[0].values

    # --------------------------------------------------

    def generate_many(self, texts):

        embeddings = []

        for text in texts:

            embedding = self.generate(
                text
            )

            embeddings.append(
                embedding
            )

        return embeddings