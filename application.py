#!/usr/bin/env python3

import re
import subprocess
import os


def parse_quiz_title(md_content):
    title_match = re.search(r"^# (.+?)$", md_content, re.MULTILINE)
    if title_match:
        return title_match.group(1).split(" - ")[-1].strip()
    return "Quiz"

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

def run_text2qti(output_file, text_files_folder):
    try:
        subprocess.run(["text2qti", os.path.join(text_files_folder, output_file)], check=True)
        print(f"text2qti has successfully converted '{output_file}' to QTI format.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running text2qti: {e}")
    except FileNotFoundError:
        print("text2qti is not installed or not found in the system path.")

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def create_output_files(md_content, lo_mappings, prefix, text_files_folder):
    create_folder(text_files_folder)
    quiz_title = parse_quiz_title(md_content)
    all_questions = set(q for qs in lo_mappings.values() for q in qs)

    # Filename prefix setup
    filename_prefix = f"{prefix}_" if prefix else "_"

    # Create a file with all questions
    all_questions_file_name = f"{filename_prefix}{quiz_title.replace(' ', '_')}.txt"
    all_questions_content = convert_md_to_text2qti(md_content, quiz_title, all_questions)
    with open(os.path.join(text_files_folder, all_questions_file_name), "w") as file:
        file.write(all_questions_content)
    print(f"All questions file created: {all_questions_file_name}")
    run_text2qti(all_questions_file_name, text_files_folder)
    # Create files for each LO
    for lo, questions in lo_mappings.items():
        # Shorten LO for filename
        short_lo = lo.split(':')[0].replace(' ', '_')
        file_name = f"{filename_prefix}{short_lo}.txt"
        quiz_content = convert_md_to_text2qti(md_content, lo, questions)
        with open(os.path.join(text_files_folder, file_name), "w") as file:
            file.write(quiz_content)
        print(f"Quiz file created: {file_name}")
        run_text2qti(file_name, text_files_folder)

def get_user_input():
    input_file = input("Please enter the name of the input file: ")
    prefix = input("Enter a prefix for the file names : ")
    return input_file, prefix

if __name__ == "__main__":
    file_name, prefix = get_user_input()
    md_content = read_file(file_name)

    if md_content:
        lo_mappings = parse_lo_mappings(md_content)
        text_files_folder = "Output_Files"  # Folder name where text files will be saved
        create_output_files(md_content, lo_mappings, prefix, text_files_folder)
    else:
        print(f"Unable to read content from '{file_name}'. Please check the file name and try again.")