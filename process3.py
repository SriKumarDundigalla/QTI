#!/usr/bin/env python3

import sys
import re
import subprocess

def convert_md_to_text2qti(md_content):
    lines = md_content.split("\n")
    question_pattern = r"^\*\*(\d+)\. (.+)$"
    answer_pattern = r"^\s+([A-D])\)\s+(.+)$"
    correct_answer_pattern = r"^\s+\*\*Answer:\s+([A-D])\)\s+(.+)$"

    current_question = None
    current_answers = []
    correct_answer = None

    qti_content = []

    for line in lines:
        question_match = re.match(question_pattern, line)
        if question_match:
            if current_question:
                qti_content.append(format_question(current_question, current_answers, correct_answer))
            
            question_number, question_text = question_match.groups()
            current_question = f"{question_number}. {question_text}"
            current_answers = []
            correct_answer = None
            continue

        answer_match = re.match(answer_pattern, line)
        if answer_match:
            answer_letter, answer_text = answer_match.groups()
            current_answers.append((answer_letter, answer_text))
            continue

        correct_answer_match = re.match(correct_answer_pattern, line)
        if correct_answer_match:
            correct_answer, _ = correct_answer_match.groups()
            continue

    if current_question:
        qti_content.append(format_question(current_question, current_answers, correct_answer))

    return "\n".join(qti_content)

def format_question(question, answers, correct_answer):
    formatted_answers = "\n".join([f"{('*' if letter == correct_answer else '')}{letter}) {text}"
                                    for letter, text in answers])
    return f"{question}\n{formatted_answers}"

def read_and_convert_file(file_name):
    try:
        with open(file_name, 'r') as file:
            md_content = file.read()
            text2qti_content = convert_md_to_text2qti(md_content)
            return text2qti_content
    except FileNotFoundError:
        print(f"The file '{file_name}' was not found.")
        return None

def run_text2qti(output_file):
    try:
        subprocess.run(["text2qti", output_file], check=True)
        print(f"text2qti has successfully converted '{output_file}' to QTI format.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running text2qti: {e}")
    except FileNotFoundError:
        print("text2qti is not installed or not found in the system path.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_reader.py <input file name> [--convert]")
    else:
        file_name = sys.argv[1]
        converted_content = read_and_convert_file(file_name)

        if converted_content:
            output_file_name = "converted_quiz.txt"
            with open(output_file_name, "w") as file:
                file.write(converted_content)
            print(f"Conversion completed. The output is saved in '{output_file_name}'")

            # Check for the '--convert' command line argument
            if '--convert' in sys.argv:
                run_text2qti(output_file_name)
