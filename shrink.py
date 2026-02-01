#!/usr/bin/env python3
from dotenv import load_dotenv
import os
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

completion = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "Was ist die Hauptstadt von Frankreich?",
        }
    ],
    temperature=1.0,
)

print(completion.choices[0].message)