import re


class DocumentChunker:
    """
    Splits documents into meaningful chunks.

    Chunks are created using paragraphs and sentences
    rather than arbitrary character positions.
    """

    def __init__(
        self,
        chunk_size=500,
        overlap=100
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    # --------------------------------------------------

    def chunk_documents(self, documents):

        chunks = []

        for document in documents:

            source = document["name"]
            text = document["text"]

            document_chunks = self._chunk_text(
                text,
                source
            )

            chunks.extend(
                document_chunks
            )

        return chunks

    # --------------------------------------------------

    def _chunk_text(
        self,
        text,
        source
    ):

        text = text.strip()

        if not text:
            return []

        paragraphs = re.split(
            r"\n\s*\n",
            text
        )

        chunks = []

        current_sentences = []
        current_length = 0

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            sentences = re.split(
                r"(?<=[.!?])\s+",
                paragraph
            )

            for sentence in sentences:

                sentence = sentence.strip()

                if not sentence:
                    continue

                sentence_length = len(sentence)

                # ----------------------------------
                # Add sentence to current chunk
                # ----------------------------------

                if (
                    current_length +
                    sentence_length +
                    1
                    <= self.chunk_size
                ):

                    current_sentences.append(
                        sentence
                    )

                    current_length += (
                        sentence_length + 1
                    )

                else:

                    # ----------------------------------
                    # Save current chunk
                    # ----------------------------------

                    if current_sentences:

                        chunk_text = "\n".join(
                            current_sentences
                        )

                        chunks.append(
                            {
                                "source": source,
                                "text": chunk_text
                            }
                        )

                    # ----------------------------------
                    # Build sentence-based overlap
                    # ----------------------------------

                    overlap_sentences = (
                        self._get_overlap_sentences(
                            current_sentences
                        )
                    )

                    current_sentences = (
                        overlap_sentences
                        + [sentence]
                    )

                    current_length = sum(
                        len(s) + 1
                        for s in current_sentences
                    )

        # ----------------------------------
        # Save final chunk
        # ----------------------------------

        if current_sentences:

            chunk_text = "\n".join(
                current_sentences
            )

            chunks.append(
                {
                    "source": source,
                    "text": chunk_text
                }
            )

        return chunks

    # --------------------------------------------------

    def _get_overlap_sentences(
        self,
        sentences
    ):

        overlap_sentences = []

        total_length = 0

        # Start from the END of the previous chunk
        # and keep complete sentences.

        for sentence in reversed(sentences):

            sentence_length = (
                len(sentence) + 1
            )

            if (
                total_length +
                sentence_length
                > self.overlap
            ):
                break

            overlap_sentences.insert(
                0,
                sentence
            )

            total_length += sentence_length

        return overlap_sentences