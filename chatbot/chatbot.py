from chatbot.client import ask_gemini
from chatbot.memory import ConversationMemory
from chatbot.prompt_manager import PromptManager
from chatbot.context_manager import ContextManager
from chatbot.profile_manager import ProfileManager
from chatbot.memory_extractor import MemoryExtractor
from chatbot.summary_manager import SummaryManager
from chatbot.summary_trigger import SummaryTrigger
from chatbot.gemini_summarizer import GeminiSummarizer
from chatbot.document_manager import DocumentManager


class ChatBot:

    def __init__(self):

        self.memory = ConversationMemory()
        self.prompt_manager = PromptManager()

        self.profile_manager = ProfileManager()
        self.memory_extractor = MemoryExtractor()

        self.summary_manager = SummaryManager()
        self.summary_trigger = SummaryTrigger()
        self.summarizer = GeminiSummarizer()

        # ---------------------------------
        # Knowledge Base
        # ---------------------------------

        self.document_manager = DocumentManager()

        # ---------------------------------
        # Context Manager
        # ---------------------------------

        self.context_manager = ContextManager(
            self.memory,
            self.prompt_manager,
            self.profile_manager,
            self.summary_manager,
            self.document_manager
        )

    # =====================================================
    # Main Chat Function
    # =====================================================

    def send_message(self, user_message):

        # ---------------------------------
        # Extract profile facts
        # ---------------------------------

        facts = self.memory_extractor.extract(user_message)

        # ---------------------------------
        # Temporary conversation history
        # ---------------------------------

        history = self.memory.get_history().copy()

        history.append(
            {
                "role": "user",
                "parts": [
                    {
                        "text": user_message
                    }
                ]
            }
        )

        # ---------------------------------
        # Build complete context
        # ---------------------------------

        context = self.context_manager.build_context(history)

        try:

            # ---------------------------------
            # Ask Gemini
            # ---------------------------------

            response = ask_gemini(context)

            # ---------------------------------
            # Save conversation
            # ---------------------------------

            self.memory.add_user_message(user_message)
            self.memory.add_bot_message(response)

            # ---------------------------------
            # Save extracted profile facts
            # ---------------------------------

            for key, value in facts.items():
                self.profile_manager.update(key, value)

            # ---------------------------------
            # Update summary
            # ---------------------------------

            self._update_summary_if_needed()

            return response

        except Exception as e:

            return (
                "⚠️ Couldn't contact Gemini.\n\n"
                f"{e}"
            )

    # =====================================================
    # Automatic Summarization
    # =====================================================

    def _update_summary_if_needed(self):

        try:

            history = self.memory.get_history()

            if not self.summary_trigger.should_summarize(history):
                return

            keep_recent = self.summary_trigger.get_keep_recent()

            old_messages = history[:-keep_recent]

            old_summary = self.summary_manager.get_summary()

            print("\n===== Messages being summarized =====")

            for message in old_messages:
                print(
                    message["role"],
                    ":",
                    message["parts"][0]["text"]
                )

            print("=====================================\n")

            new_summary = self.summarizer.summarize(
                old_summary,
                old_messages
            )

            self.summary_manager.update_summary(
                new_summary
            )

            self.memory.trim_history(
                keep_recent
            )

            print("✓ Conversation summarized.")

        except Exception as e:

            print(
                f"Summary update failed: {e}"
            )