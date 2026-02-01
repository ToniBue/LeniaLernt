#!/usr/bin/env python3
"""
Ein einfaches Quiz-Programm (sehr grundlegend).
Keine Funktionen, keine f-Strings, keine enumerate, und für Optionen jeweils 4 separate print-Anweisungen.
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

# Sehr einfache, lineare Ausführung ohne Funktionen
score = 0
total = len(questions)
idx = 0

while idx < total:
    print("\nFrage " + str(idx + 1) + ": " + questions[idx])
    # Keine Schleife für Optionen - vier einzelne print-Anweisungen
    print("  1. " + options[idx][0])
    print("  2. " + options[idx][1])
    print("  3. " + options[idx][2])
    print("  4. " + options[idx][3])

    while True:
        reply = input("Deine Antwort (1-4): ").strip()
        if reply.isdigit():
            n = int(reply)
            if 1 <= n <= 4:
                if (n - 1) == answers[idx]:
                    print("Richtig! " + "✅")
                    score = score + 1
                else:
                    print("Falsch. Die richtige Antwort ist: " + options[idx][answers[idx]])
                break
        print("Ungültige Eingabe. Bitte gib eine Zahl von 1 bis 4 ein.")

    idx = idx + 1

print("\n---")
print("Ergebnis: " + str(score) + " von " + str(total) + " richtig. (" + str(int(score / total * 100)) + "%)")
