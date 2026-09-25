import json
import time

from google import genai
from google.genai import types

from chatbot.config import API_KEY, MODEL_NAME
from chatbot.context_serializer import ContextSerializer

client = genai.Client(api_key=API_KEY)

serializer = ContextSerializer()


# =====================================================
# Private Request Helper
# =====================================================

def _generate_content(contents, config):

    last_exception = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=config
            )

            return response.text

        except Exception as e:

            last_exception = e

            error = str(e)

            if "503" in error or "UNAVAILABLE" in error:

                wait_time = 2 ** attempt

                print(
                    f"Gemini unavailable. "
                    f"Retrying in {wait_time} second(s)..."
                )

                time.sleep(wait_time)
                continue

            raise

    raise last_exception


# =====================================================
# Chat
# =====================================================

def ask_gemini(context):

    system_prompt, messages = serializer.serialize(context)

    config = types.GenerateContentConfig(
        system_instruction=system_prompt
    )

    return _generate_content(
        messages,
        config
    )


# =====================================================
# Summarization
# =====================================================

def summarize_conversation(prompt):

    config = types.GenerateContentConfig(
        temperature=0.2
    )

    return _generate_content(
        prompt,
        config
    )


# =====================================================
# Memory Extraction
# =====================================================

def extract_memory(prompt):

    config = types.GenerateContentConfig(
        temperature=0
    )

    response = _generate_content(
        prompt,
        config
    )

    try:
        return json.loads(response)
    except Exception:
        return {}