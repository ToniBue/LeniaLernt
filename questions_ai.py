#!/usr/bin/env python3
"""Generate a single multiple-choice quiz question on a given topic.

Function provided:
- generate_quiz_question(topic: str) -> dict
  Returns: {"question": str, "options": [str, str, str, str], "answer_index": int}

The function calls the configured OpenAI (or Azure OpenAI) deployment and expects a JSON response from the model.
"""
from dotenv import load_dotenv
import json
import os
import re
from typing import Dict, List
from openai import OpenAI

# Load environment variables from .env (if present)
load_dotenv()

endpoint = os.environ.get(
    "AZURE_EXISTING_AIPROJECT_ENDPOINT",
    "https://daniel-schmode-novel-resource.openai.azure.com/openai/v1/",
)
deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME", "gpt-5.2-chat")
api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_API_KEY")

if not api_key:
    raise RuntimeError(
        "API key not found. Please set OPENAI_API_KEY or AZURE_OPENAI_API_KEY in your environment or in a local .env file."
    )

client = OpenAI(base_url=endpoint, api_key=api_key)


def _extract_json(text: str) -> str:
    """Try to extract the first JSON object from text."""
    match = re.search(r"({[\s\S]*})", text)
    return match.group(1) if match else text


def generate_quiz_question(topic: str, language: str = "deutsch") -> Dict[str, object]:
    """Generate a multiple-choice quiz question for a given topic in the given language.

    Parameters:
        topic: non-empty string describing the quiz topic
        language: language name (e.g., "deutsch" for German, "english" for English)

    The returned dict has the shape:
    {
        "question": "...",
        "options": ["opt1", "opt2", "opt3", "opt4"],
        "answer_index": 0  # integer index into options (0-3)
    }

    Raises a ValueError if the model response cannot be parsed or doesn't match expectations.
    """

    if not topic or not topic.strip():
        raise ValueError("Topic must be a non-empty string")

    prompt = (
        "You are a helpful assistant that creates single multiple-choice quiz questions. "
        "Return ONLY a JSON object with three keys: 'question' (string), 'options' (list of exactly 4 strings), "
        "and 'answer_index' (integer with value 0-3 indicating the correct option index). "
        f"Create a concise, clear question about the topic: '{topic}'. "
        f"Return the question and options in the following language: '{language}'. "
        "Do not add any extra text or explanation; the output must be valid JSON only."
    )

    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )

    # Extract the textual content from the response
    raw_msg = completion.choices[0].message
    if isinstance(raw_msg, dict):
        text = raw_msg.get("content", "")
    else:
        text = getattr(raw_msg, "content", str(raw_msg))

    # Try to get JSON content
    json_text = _extract_json(text)

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON from model response: {exc}\nResponse text: {text}") from exc

    # Basic validation
    if not isinstance(payload, dict):
        raise ValueError("Parsed JSON must be an object")

    question = payload.get("question")
    options = payload.get("options")
    answer_index = payload.get("answer_index")

    if not isinstance(question, str) or not question.strip():
        raise ValueError("'question' must be a non-empty string")

    if not isinstance(options, list) or len(options) != 4 or not all(isinstance(o, str) for o in options):
        raise ValueError("'options' must be a list of exactly 4 strings")

    if not isinstance(answer_index, int) or not (0 <= answer_index < 4):
        raise ValueError("'answer_index' must be an integer between 0 and 3")

    return {"question": question.strip(), "options": [o.strip() for o in options], "answer_index": answer_index}


if __name__ == "__main__":
    # Quick demo
    topic = input("Enter a topic for a quiz question (e.g., 'geography', 'python programming'): ") or "geography"
    language = input("Output language (e.g., 'deutsch' for German) [default: deutsch]: ") or "deutsch"
    try:
        quiz = generate_quiz_question(topic, language=language)
        print(json.dumps(quiz, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
