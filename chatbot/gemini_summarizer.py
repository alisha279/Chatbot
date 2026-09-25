from chatbot.client import summarize_conversation


class GeminiSummarizer:
    """
    Generates conversation summaries using Gemini.

    Responsibility:
        Existing Summary
                +
        Conversation Messages
                ↓
          Updated Summary
    """

    # --------------------------------------------------

    def summarize(
        self,
        old_summary,
        messages
    ):

        prompt = self._build_prompt(
            old_summary,
            messages
        )

        response = summarize_conversation(
            prompt
        )

        return self._clean_response(
            response
        )

    # --------------------------------------------------

    def _build_prompt(
        self,
        old_summary,
        messages
    ):

        conversation = self._format_messages(
            messages
        )

        return f"""
You are a conversation summarization assistant.

Your task is to update an existing summary using the latest conversation.

Rules:

- Preserve important long-term facts.
- Remove unnecessary details.
- Ignore greetings and small talk.
- Keep the summary under 300 words.
- Write in clear English.
- Return ONLY the summary.

Existing Summary:

{old_summary}

Conversation:

{conversation}
"""

    # --------------------------------------------------

    def _format_messages(
        self,
        messages
    ):

        lines = []

        for message in messages:

            role = message["role"]
            text = message["parts"][0]["text"]

            if role == "user":
                role = "User"
            else:
                role = "Assistant"

            lines.append(
                f"{role}: {text}"
            )

        return "\n".join(lines)

    # --------------------------------------------------

    def _clean_response(
        self,
        response
    ):

        return response.strip()