import re


class MemoryRetriever:
    """
    Retrieves relevant past conversations.

    Instead of scoring every message individually,
    we score only user questions and return both
    the user message and the assistant reply.
    """

    def __init__(self, top_k=3):

        self.top_k = top_k

    # ==================================================

    def retrieve(self, query, messages):

        keywords = self._extract_keywords(query)

        if not keywords:
            return []

        pairs = self._build_pairs(messages)

        scored_pairs = []

        for pair in pairs:

            score = self._score(
                pair["user"]["parts"][0]["text"],
                keywords
            )

            if score > 0:

                scored_pairs.append(
                    (
                        score,
                        pair
                    )
                )

        scored_pairs.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        retrieved = []

        print("\n===== Retrieved Memories =====")

        for score, pair in scored_pairs[:self.top_k]:

            print(
                f"[Score {score}]",
                pair["user"]["parts"][0]["text"]
            )

            retrieved.append(pair["user"])

            if pair["assistant"] is not None:
                retrieved.append(pair["assistant"])

        print("==============================\n")

        return retrieved

    # ==================================================

    def _build_pairs(self, messages):

        pairs = []

        i = 0

        while i < len(messages):

            current = messages[i]

            if current["role"] != "user":
                i += 1
                continue

            assistant = None

            if (
                i + 1 < len(messages)
                and messages[i + 1]["role"] == "model"
            ):
                assistant = messages[i + 1]

            pairs.append(
                {
                    "user": current,
                    "assistant": assistant
                }
            )

            i += 2

        return pairs

    # ==================================================

    def _extract_keywords(self, text):

        words = re.findall(
            r"[A-Za-z]+",
            text.lower()
        )

        stop_words = {
            "the",
            "a",
            "an",
            "is",
            "are",
            "what",
            "who",
            "how",
            "why",
            "where",
            "when",
            "again",
            "please",
            "tell",
            "define",
            "explain",
            "about",
            "can",
            "could",
            "would",
            "i",
            "you",
            "my",
            "your",
            "me",
            "to",
            "of",
            "for"
        }

        return [
            word
            for word in words
            if word not in stop_words
        ]

    # ==================================================

    def _score(
        self,
        text,
        keywords
    ):

        text = text.lower()

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 5

        return score