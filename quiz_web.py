#!/usr/bin/env python3
"""
Ein einfaches Quiz mit Streamlit (Browser).
streamlit run quiz_web.py 
"""

import streamlit as st

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

answers = [3, 1, 1, 1, 2]

if "idx" not in st.session_state:
    st.session_state.idx = 0
    st.session_state.score = 0
    # Zustand für Button-basiertes Quiz
    st.session_state.answered = False
    st.session_state.last_correct = False
    st.session_state.last_answer = None

idx = st.session_state.idx

st.title("Quiz")

# Callback-Funktionen für Button-basierte Aktionen
def _answer(i, qidx):
    # Setze Ergebnis für die aktuelle Frage
    st.session_state.answered = True
    st.session_state.last_correct = (i == answers[qidx])
    if i == answers[qidx]:
        st.session_state.score += 1
    st.session_state.last_answer = i

def _next():
    st.session_state.idx += 1
    st.session_state.answered = False
    st.session_state.last_answer = None
    st.session_state.last_correct = False

def _reset():
    st.session_state.idx = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_answer = None
    st.session_state.last_correct = False


if idx < len(questions):
    st.subheader("Frage " + str(idx + 1))
    st.write(questions[idx])
    # Antwort-Buttons direkt anzeigen
    if "answered" not in st.session_state or not st.session_state.answered:
        for i, opt in enumerate(options[idx]):
            # Verwende on_click Callback, damit die Aktion beim ersten Klick ausgeführt wird
            st.button(opt, key=f"btn_{idx}_{i}", on_click=_answer, args=(i, idx))
    else:
        # Feedback anzeigen
        if st.session_state.last_correct:
            st.success("Richtig! ✅")
        else:
            st.error("Falsch. Richtige Antwort: " + options[idx][answers[idx]])
        if st.button("Nächste Frage", key=f"next_{idx}", on_click=_next):
            pass  # on_click Callback übernimmt das Fortschalten
else:
    st.write("Ergebnis: " + str(st.session_state.score) + " von " + str(len(questions)) + " richtig.")
    if st.button("Noch einmal", on_click=_reset):
        pass  # _reset setzt den Zustand zurück