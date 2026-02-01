#!/usr/bin/env python3
"""Interactive German-language chatbot acting as an empathetic, mindful and slightly humorous psychologist.

Usage: python shrink_chat.py
"""
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

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "Du bist ein einfühlsamer Psychologe, der freundlich, achtsam und mit gutem Humor antwortet. "
        "Antworte ausschließlich auf Deutsch. Zeige Empathie, stelle offene Fragen und biete kleine Achtsamkeitsimpulse an. "
        "Verwende behutsamen Humor, um die Stimmung zu heben, aber bleibe respektvoll. "
        "Wichtig: Du bist kein Ersatz für professionelle medizinische oder psychiatrische Hilfe. "
        "Wenn die Person Anzeichen von Krise oder Selbstgefährdung zeigt, ermutige sie, sofort professionelle Hilfe oder lokale Notdienste zu kontaktieren, "
        "und vermeide detaillierte Anleitungen zur Selbstschädigung. Antworte kurz, klar und fürsorglich."
    ),
}


def chat_loop():
    print("Hallo! Ich bin dein achtsamer und humorvoller Gesprächspartner. (Tippe 'exit' oder 'quit' zum Beenden)")
    print("Hinweis: Ich bin kein Ersatz für professionelle Hilfe. Bei akuten Krisen wende dich bitte an lokale Notdienste.")

    messages = [SYSTEM_MESSAGE]

    while True:
        try:
            user_input = input("Du: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAuf Wiedersehen — pass gut auf dich auf!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye", "ende"):
            print("Auf Wiedersehen — viel Kraft und alles Gute!")
            break

        messages.append({"role": "user", "content": user_input})

        # Begrenze Verlaufslänge
        if len(messages) > 20:
            messages = [messages[0]] + messages[-18:]

        try:
            completion = client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                temperature=0.7,
            )
        except Exception as e:
            print(f"Fehler beim Abrufen der Antwort: {e}")
            continue

        raw_msg = completion.choices[0].message
        if isinstance(raw_msg, dict):
            reply = raw_msg.get("content", "")
        else:
            reply = getattr(raw_msg, "content", str(raw_msg))

        reply = reply.strip()
        print("\nBot:", reply, "\n")

        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat_loop()
