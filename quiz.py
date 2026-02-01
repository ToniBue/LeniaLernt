#!/usr/bin/env python3
"""
Ein einfaches Quiz-Programm.
Fragen, mögliche Antworten und der Index der richtigen Antwort werden in Listen gespeichert.
Jede Frage hat genau 4 Antwortmöglichkeiten.
"""

questions = [
    "Wie viele Kontinente gibt es auf der Erde?",
    "Was ist die Hauptstadt von Deutschland?",
    "Welches Element hat das chemische Symbol 'O'?",
    "Welches Jahr begann der Erste Weltkrieg?",
    "Welche Programmiersprache wird oft für Datenanalyse und Machine Learning verwendet?",
]

options = [
    ["4", "5", "6", "7"],
    ["München", "Berlin", "Hamburg", "Köln"],
    ["Gold", "Sauerstoff", "Silber", "Wasserstoff"],
    ["1912", "1914", "1916", "1918"],
    ["C++", "Ruby", "Python", "HTML"],
]

# Index der korrekten Antworten (0-basiert)
answers = [3, 1, 1, 1, 2]


def ask_question(index: int) -> bool:
    """Gibt eine Frage aus und fragt die Nutzerin/den Nutzer nach einer Antwort.
    Rückgabe True, wenn korrekt, sonst False.
    """
    print(f"\nFrage {index + 1}: {questions[index]}")
    for i, opt in enumerate(options[index], start=1):
        print(f"  {i}. {opt}")

    while True:
        reply = input("Deine Antwort (1-4): ").strip()
        if reply.isdigit():
            n = int(reply)
            if 1 <= n <= 4:
                return (n - 1) == answers[index]
        print("Ungültige Eingabe. Bitte gib eine Zahl von 1 bis 4 ein.")


def run_quiz():
    """Führt das Quiz durch und gibt das Ergebnis aus."""
    score = 0
    total = len(questions)

    for idx in range(total):
        correct = ask_question(idx)
        if correct:
            print("Richtig! ✅")
            score += 1
        else:
            correct_ans = options[idx][answers[idx]]
            print(f"Falsch. Die richtige Antwort ist: {correct_ans}")

    print("\n---")
    print(f"Ergebnis: {score} von {total} richtig. ({score / total * 100:.0f}%)")


if __name__ == "__main__":
    run_quiz()
