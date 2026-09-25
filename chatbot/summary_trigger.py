class SummaryTrigger:

    def __init__(
        self,
        max_messages=12,
        keep_recent=4,
        enabled=True,
    ):
        self.enabled = enabled
        self.max_messages = max_messages
        self.keep_recent = keep_recent

    # -----------------------------

    def should_summarize(self, messages):

        if not self.enabled:
            return False

        return self.message_limit_reached(messages)

    # -----------------------------

    def message_limit_reached(self, messages):
        return len(messages) >= self.max_messages

    # -----------------------------

    def get_keep_recent(self):
        return self.keep_recent

    # -----------------------------

    def enable(self):
        self.enabled = True

    # -----------------------------

    def disable(self):
        self.enabled = False

    # -----------------------------

    def is_enabled(self):
        return self.enabled