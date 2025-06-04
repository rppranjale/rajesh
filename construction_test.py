# -*- coding: utf-8 -*-
"""Construction Site Supervision Competency Test.

Run this script to take a short multiple choice test. At the end of the
quiz a PDF report will be generated with the results.

Usage::

    python3 construction_test.py

Dependencies:
    - fpdf2

Install dependencies using:

    pip install fpdf2
"""
from dataclasses import dataclass
from typing import List

try:
    from fpdf import FPDF
except ImportError as exc:  # pragma: no cover - dependency check
    raise SystemExit(
        "The fpdf2 package is required. Install it with 'pip install fpdf2'"
    ) from exc


@dataclass
class Question:
    text: str
    options: List[str]
    answer_index: int
    explanation: str


QUESTIONS = [
    Question(
        text="What is the primary role of a site supervisor?",
        options=[
            "A) Perform structural design",
            "B) Manage on-site safety and operations",
            "C) Purchase materials",
            "D) Handle corporate accounting",
        ],
        answer_index=1,
        explanation=(
            "A site supervisor oversees daily site operations and ensures that "
            "work is carried out safely and according to plans."
        ),
    ),
    Question(
        text="When should a toolbox talk typically be held?",
        options=[
            "A) At project completion",
            "B) Before the start of the shift",
            "C) During lunch breaks",
            "D) After accidents only",
        ],
        answer_index=1,
        explanation=(
            "Toolbox talks are short safety meetings held before work begins to "
            "discuss potential hazards and safe practices."
        ),
    ),
    Question(
        text="Which document outlines the hazards and controls for a specific task?",
        options=[
            "A) Bill of quantities",
            "B) Method statement",
            "C) Purchase order",
            "D) Time sheet",
        ],
        answer_index=1,
        explanation=(
            "A method statement describes how a particular job should be "
            "performed safely, detailing hazards and control measures."
        ),
    ),
]


def ask_questions() -> List[int]:
    """Prompt the user for answers and return their choices."""
    answers = []
    print("Construction Site Supervision Competency Test\n")
    for i, q in enumerate(QUESTIONS, start=1):
        print(f"Question {i}: {q.text}")
        for option in q.options:
            print(option)
        choice = input("Your answer (A/B/C/D): ").strip().upper()
        while choice not in {"A", "B", "C", "D"}:
            choice = input("Please enter A, B, C or D: ").strip().upper()
        answers.append(["A", "B", "C", "D"].index(choice))
        print()
    return answers


def generate_report(answers: List[int], filename: str = "test_report.pdf") -> None:
    """Generate a PDF report with results and explanations."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(0, 10, "Construction Site Supervision Competency Test", ln=True)

    pdf.set_font("Helvetica", size=12)
    score = sum(ans == q.answer_index for ans, q in zip(answers, QUESTIONS))
    pdf.ln(5)
    pdf.cell(0, 10, f"Score: {score} / {len(QUESTIONS)}", ln=True)
    pdf.ln(5)

    for i, (ans, q) in enumerate(zip(answers, QUESTIONS), start=1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, f"Question {i}", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.multi_cell(0, 10, q.text)
        pdf.ln(1)
        pdf.cell(0, 10, f"Your answer: {q.options[ans]}", ln=True)
        correct_option = q.options[q.answer_index]
        if ans == q.answer_index:
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 10, "Correct!", ln=True)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, "Incorrect", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, f"Correct answer: {correct_option}", ln=True)
        pdf.multi_cell(0, 10, f"Explanation: {q.explanation}")
        pdf.ln(5)

    pdf.output(filename)
    print(f"Detailed report saved to {filename}")


def main() -> None:
    user_answers = ask_questions()
    score = sum(ans == q.answer_index for ans, q in zip(user_answers, QUESTIONS))
    print(f"\nYou scored {score} out of {len(QUESTIONS)}")
    generate_report(user_answers)


if __name__ == "__main__":
    main()
