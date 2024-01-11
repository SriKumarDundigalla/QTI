#!/usr/bin/env python3

import sys
import re
import subprocess
import os

def parse_lo_mappings(md_content):
    mapping_section = re.search(r"## Mapping of LO's to questions\n\n[\s\S]+?\|\n([\s\S]+)", md_content)
    if not mapping_section:
        print("No Learning Outcomes mappings found.")
        return {}

    mapping_lines = mapping_section.group(1).split("\n")[1:]  # Skip the first line (header separator)
    lo_mappings = {}
    for line in mapping_lines:
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 3:
                lo = parts[1].strip()
                questions = [q.strip() for q in parts[2].split(",")]
                lo_mappings[lo] = questions
    return lo_mappings


def convert_md_to_text2qti(md_content, lo, questions):
    lines = md_content.split("\n")
    question_pattern = r"^\*\*(\d+)\.\s*(.+?)\*\*$"
    answer_pattern = r"^\s+([A-D])\)\s+(.+)$"
    correct_answer_pattern = r"^\s+\*\*Answer:\s+([A-D])\)\s+(.+)$"

    qti_content = {}
    current_question = None
    current_answers = []
    correct_answer = None

    for line in lines:
        question_match = re.match(question_pattern, line)
        if question_match:
            question_number, question_text = question_match.groups()
            if question_number in questions:
                current_question_number = question_number
                current_question = f"{question_number}. {question_text}"
                current_answers = []
                correct_answer = None

        answer_match = re.match(answer_pattern, line)
        if answer_match and current_question:
            answer_letter, answer_text = answer_match.groups()
            current_answers.append((answer_letter, answer_text))

        correct_answer_match = re.match(correct_answer_pattern, line)
        if correct_answer_match and current_question:
            correct_answer, _ = correct_answer_match.groups()
            qti_content[current_question_number] = format_question(current_question, current_answers, correct_answer)
            current_question = None

    # Format quiz content for text2qti
    quiz_content = [f"Quiz title: {lo}\n"]
    for q_num in questions:
        if q_num in qti_content:
            quiz_content.append(qti_content[q_num] + "\n")

    return "\n".join(quiz_content)

def format_question(question, answers, correct_answer):
    formatted_answers = "\n".join([f"{('*' if letter == correct_answer else '')}{letter}) {text}"
                                    for letter, text in answers])
    return f"{question}\n{formatted_answers}"

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
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

def create_output_files(md_content, lo_mappings):
    for lo, questions in lo_mappings.items():
        file_name = f"{lo.replace(' ', '_')}.txt"
        quiz_content = convert_md_to_text2qti(md_content, lo, questions)
        with open(file_name, "w") as file:
            file.write(quiz_content)
        print(f"Quiz file created: {file_name}")
        run_text2qti(file_name)

def get_user_input():
    return input("Please enter the name of the input file: ")

if __name__ == "__main__":
    file_name = get_user_input()
    md_content = read_file(file_name)

    if md_content:
        lo_mappings = parse_lo_mappings(md_content)
        create_output_files(md_content, lo_mappings)
    else:
        print(f"Unable to read content from '{file_name}'. Please check the file name and try again.")