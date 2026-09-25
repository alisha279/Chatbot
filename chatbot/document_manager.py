from pathlib import Path

from chatbot.document_chunker import DocumentChunker
from chatbot.embedding_generator import EmbeddingGenerator


class DocumentManager:
    """
    Loads learning documents, chunks them,
    and generates embeddings for each chunk.

    Pipeline:

        knowledge/*.txt
                ↓
        DocumentChunker
                ↓
        Chunks
                ↓
        EmbeddingGenerator
                ↓
        Chunks + Embeddings
    """

    def __init__(
        self,
        knowledge_folder="knowledge"
    ):

        self.knowledge_folder = Path(
            knowledge_folder
        )

        self.chunker = DocumentChunker()

        self.embedding_generator = (
            EmbeddingGenerator()
        )

        self.chunks = []

        self.load_documents()

    # --------------------------------------------------

    def load_documents(self):

        self.chunks.clear()

        if not self.knowledge_folder.exists():
            return

        for file in self.knowledge_folder.glob("*.txt"):

            text = file.read_text(
                encoding="utf-8"
            )

            documents = [
                {
                    "name": file.name,
                    "text": text
                }
            ]

            chunks = self.chunker.chunk_documents(
                documents
            )

            for chunk in chunks:

                embedding = (
                    self.embedding_generator.generate(
                        chunk["text"]
                    )
                )

                self.chunks.append(
                    {
                        "source": chunk["source"],
                        "text": chunk["text"],
                        "embedding": embedding
                    }
                )

    # --------------------------------------------------

    def reload(self):

        self.load_documents()

    # --------------------------------------------------

    def get_chunks(self):

        return self.chunks.copy()

    # --------------------------------------------------

    def number_of_documents(self):

        return len(
            list(
                self.knowledge_folder.glob("*.txt")
            )
        )

    # --------------------------------------------------

    def number_of_chunks(self):

        return len(self.chunks)