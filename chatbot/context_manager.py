from chatbot.models import Context
from chatbot.memory_retriever import MemoryRetriever
from chatbot.document_retriever import DocumentRetriever


class ContextManager:

    def __init__(
        self,
        memory,
        prompt_manager,
        profile_manager,
        summary_manager,
        document_manager
    ):

        self.memory = memory
        self.prompt_manager = prompt_manager
        self.profile_manager = profile_manager
        self.summary_manager = summary_manager
        self.document_manager = document_manager

        self.memory_retriever = MemoryRetriever()
        self.document_retriever = DocumentRetriever()

    # ---------------------------------

    def build_context(self, messages=None):

        if messages is None:
            messages = self._get_messages()

        latest_message = ""

        if messages:
            latest_message = messages[-1]["parts"][0]["text"]

        retrieved_memories = self.memory_retriever.retrieve(
            latest_message,
            self.memory.get_history()
        )

        retrieved_documents = self.document_retriever.retrieve(
            latest_message,
            self.document_manager.get_chunks()
        )

        return Context(
            system_prompt=self._get_system_prompt(),
            messages=messages,
            summary=self._get_summary(),
            user_profile=self._get_user_profile(),
            retrieved_memories=retrieved_memories,
            documents=retrieved_documents
        )

    # ---------------------------------

    def _get_system_prompt(self):
        return self.prompt_manager.get_prompt()

    # ---------------------------------

    def _get_messages(self):
        return self.memory.get_history()

    # ---------------------------------

    def _get_user_profile(self):
        return self.profile_manager.get_profile()

    # ---------------------------------

    def _get_summary(self):
        return self.summary_manager.get_summary()