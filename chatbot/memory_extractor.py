import json

from chatbot.client import extract_memory


class MemoryExtractor:

    def extract(self, message):

        prompt = self._build_prompt(message)

        return extract_memory(prompt)

    # =====================================================

    def _build_prompt(self, message):

        return f"""
You are a memory extraction system.

Your task is to extract ONLY long-term user profile facts.

Extract only if explicitly stated.

Examples of valid facts:

- name
- education
- university
- favorite_language
- profession
- country
- city

Ignore:

- questions
- temporary moods
- requests
- explanations
- greetings
- ongoing tasks
- things the assistant says

Return ONLY valid JSON.

Examples

User:
My name is Alisha.

Output:
{{
    "name":"Alisha"
}}

User:
I study BSCS at QAU.

Output:
{{
    "education":"BSCS",
    "university":"QAU"
}}

User:
Python is my favorite language.

Output:
{{
    "favorite_language":"Python"
}}

User:
I am building an AI chatbot.

Output:
{{}}

Now extract facts.

User:

{message}
"""