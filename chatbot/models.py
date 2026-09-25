from dataclasses import dataclass, field


@dataclass
class Context:
    """
    Represents the complete context
    that will be sent to the LLM.
    """ 

    system_prompt: str
    messages: list

    summary: str = ""

    user_profile: dict = field(default_factory=dict)
    
    retrieved_memories: list = field(default_factory=list)

    documents: list = field(default_factory=list)

    tool_results: list = field(default_factory=list)