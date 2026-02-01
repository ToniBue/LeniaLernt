#!/usr/bin/env python3
"""
Ein einfaches Quiz mit einer Tkinter-GUI.

Starten: python3 quiz_gui.py
"""

import tkinter as tk
from tkinter import messagebox

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


class QuizGUI:
    def __init__(self, master):
        self.master = master
        master.title("Quiz")
        master.resizable(False, False)

        self.idx = 0
        self.score = 0

        self.question_label = tk.Label(master, text="", wraplength=380, justify="left", font=(None, 12))
        self.question_label.pack(padx=10, pady=(10, 5))

        self.var = tk.IntVar(value=-1)

        self.rb1 = tk.Radiobutton(master, text="", variable=self.var, value=0, anchor="w", justify="left")
        self.rb1.pack(fill="x", padx=20)
        self.rb2 = tk.Radiobutton(master, text="", variable=self.var, value=1, anchor="w", justify="left")
        self.rb2.pack(fill="x", padx=20)
        self.rb3 = tk.Radiobutton(master, text="", variable=self.var, value=2, anchor="w", justify="left")
        self.rb3.pack(fill="x", padx=20)
        self.rb4 = tk.Radiobutton(master, text="", variable=self.var, value=3, anchor="w", justify="left")
        self.rb4.pack(fill="x", padx=20)

        self.feedback_label = tk.Label(master, text="", fg="blue")
        self.feedback_label.pack(pady=(5, 0))

        btn_frame = tk.Frame(master)
        btn_frame.pack(fill="x", pady=10)

        self.next_btn = tk.Button(btn_frame, text="Nächste Frage", command=self.next_question)
        self.next_btn.pack(side="right", padx=10)

        self.score_label = tk.Label(btn_frame, text="Punktzahl: 0")
        self.score_label.pack(side="left", padx=10)

        # Zeige erste Frage
        self.show_question()

        master.bind("<Return>", lambda event: self.next_question())

    def show_question(self):
        if self.idx < len(questions):
            self.question_label.config(text=f"Frage {self.idx + 1}: {questions[self.idx]}")
            self.rb1.config(text="1. " + options[self.idx][0])
            self.rb2.config(text="2. " + options[self.idx][1])
            self.rb3.config(text="3. " + options[self.idx][2])
            self.rb4.config(text="4. " + options[self.idx][3])
            self.var.set(-1)
            self.feedback_label.config(text="")
            self.score_label.config(text="Punktzahl: " + str(self.score))
            self.next_btn.config(text="Nächste Frage")
        else:
            self.finish_quiz()

    def next_question(self):
        if self.idx >= len(questions):
            self.finish_quiz()
            return

        choice = self.var.get()
        if choice not in (0, 1, 2, 3):
            messagebox.showwarning("Hinweis", "Bitte wähle eine Antwort (1-4).")
            return

        if choice == answers[self.idx]:
            self.score += 1
            self.feedback_label.config(text="Richtig! ✅", fg="green")
        else:
            correct = options[self.idx][answers[self.idx]]
            self.feedback_label.config(text=f"Falsch. Richtig wäre: {correct}", fg="red")

        self.idx += 1
        if self.idx < len(questions):
            self.next_btn.config(text="Weiter")
            # kleine Verzögerung, damit Nutzer das Feedback sehen kann
            self.master.after(800, self.show_question)
        else:
            self.master.after(800, self.finish_quiz)

    def finish_quiz(self):
        pct = int(self.score / len(questions) * 100)
        msg = f"Ergebnis: {self.score} von {len(questions)} richtig. ({pct}%)"
        if messagebox.askyesno("Quiz beendet", msg + "\n\nMöchtest du noch einmal spielen?"):
            self.idx = 0
            self.score = 0
            self.show_question()
        else:
            self.master.quit()


if __name__ == "__main__":
    root = tk.Tk()
    # Fenstergröße begrenzen, damit Zeilenumbruch bei langen Fragen funktioniert
    root.geometry("420x260")
    app = QuizGUI(root)
    root.mainloop()
