import math

from chatbot.embedding_generator import EmbeddingGenerator


class DocumentRetriever:

    def __init__(
        self,
        top_k=3,
        similarity_threshold=0.65
    ):

        self.top_k = top_k
        self.similarity_threshold = (
            similarity_threshold
        )

        self.embedding_generator = (
            EmbeddingGenerator()
        )

    # --------------------------------------------------

    def retrieve(
        self,
        query,
        chunks
    ):

        if not query:
            return []

        if not chunks:
            return []

        query_embedding = (
            self.embedding_generator.generate(
                query
            )
        )

        scored_chunks = []

        for chunk in chunks:

            embedding = chunk.get(
                "embedding"
            )

            if not embedding:
                continue

            score = self._cosine_similarity(
                query_embedding,
                embedding
            )

            # Only keep genuinely relevant chunks
            if score >= self.similarity_threshold:

                scored_chunks.append(
                    (
                        score,
                        chunk
                    )
                )

        scored_chunks.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        return [
            chunk
            for score, chunk
            in scored_chunks[:self.top_k]
        ]

    # --------------------------------------------------

    def _cosine_similarity(
        self,
        vector_a,
        vector_b
    ):

        if not vector_a or not vector_b:
            return 0.0

        dot_product = sum(
            a * b
            for a, b in zip(
                vector_a,
                vector_b
            )
        )

        magnitude_a = math.sqrt(
            sum(
                a * a
                for a in vector_a
            )
        )

        magnitude_b = math.sqrt(
            sum(
                b * b
                for b in vector_b
            )
        )

        if (
            magnitude_a == 0
            or magnitude_b == 0
        ):

            return 0.0

        return (
            dot_product /
            (
                magnitude_a *
                magnitude_b
            )
        )