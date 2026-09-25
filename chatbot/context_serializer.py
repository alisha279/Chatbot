class ContextSerializer:
    """
    Converts a Context object into the format expected
    by the Gemini client.
    """

    def serialize(self, context):

        system_prompt = self._build_system_prompt(context)
        messages = context.messages

        return system_prompt, messages

    # -------------------------------------------------

    def _build_system_prompt(self, context):

        sections = [
            context.system_prompt.strip()
        ]

        summary = self._format_summary(
            context.summary
        )

        if summary:
            sections.append(summary)

        profile = self._format_profile(
            context.user_profile
        )

        if profile:
            sections.append(profile)

        memories = self._format_memories(
            context.retrieved_memories
        )

        if memories:
            sections.append(memories)

        documents = self._format_documents(
            context.documents
        )

        if documents:
            sections.append(documents)

        return "\n\n".join(sections)

    # -------------------------------------------------

    def _format_summary(self, summary):

        if not summary:
            return ""

        return (
            "Conversation Summary:\n"
            f"{summary}"
        )

    # -------------------------------------------------

    def _format_profile(self, profile):

        if not profile:
            return ""

        lines = [
            "Known information about the user:"
        ]

        for key, value in profile.items():

            label = (
                key
                .replace("_", " ")
                .title()
            )

            lines.append(
                f"- {label}: {value}"
            )

        return "\n".join(lines)

    # -------------------------------------------------

    def _format_memories(self, memories):

        if not memories:
            return ""

        lines = [
            "Relevant Previous Conversation:"
        ]

        for message in memories:

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

    # -------------------------------------------------

    def _format_documents(self, documents):

        if not documents:
            return ""

        lines = [
            "Relevant Study Material:"
        ]

        for document in documents:

            lines.append("")
            lines.append(
                f"Source: {document['source']}"
            )

            lines.append(
                document["text"]
            )
            
        
        
        return "\n".join(lines)