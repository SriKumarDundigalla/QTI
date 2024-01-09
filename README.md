# Markdown to text2qti Converter

This Python script is designed to convert Markdown (.md) files, specifically formatted with quiz questions and answers, into a format compatible with the `text2qti` package. `text2qti` is a tool that converts text files into quizzes in the QTI (Question and Test Interoperability) format, suitable for various learning management systems (LMS).

## Features

- Reads Markdown files with specific quiz question formatting.
- Converts quiz content into text2qti-compatible format.
- Provides an option to automatically convert the generated text file to QTI format using `text2qti`.

## How It Works

The script performs the following steps:

1. **Reading the Markdown File:**
   - The file specified as a command-line argument is read.
   - If the file is not found, an error message is displayed.

2. **Converting Markdown to text2qti Format:**
   - The content is parsed and converted into a format that `text2qti` can understand.
   - The conversion is done using regular expressions to identify questions, answers, and the correct choice.

3. **Writing to a New File:**
   - The converted content is written to a new text file (`converted_quiz.txt`).

4. **Optional Conversion to QTI Format:**
   - If the `--convert` flag is used, the script additionally runs the `text2qti` command on the generated text file to produce a QTI file.

## Regular Expressions Explained

The script uses Python's `re` module for parsing the Markdown content. Here are the regular expressions used:

1. `question_pattern = r"^\*\*(\d+)\. (.+)$"`:
   - This regex matches lines starting with double asterisks, a number, a period, and the question text.
   - Captures the question number and text.

2. `answer_pattern = r"^\s+([A-D])\)\s+(.+)$"`:
   - Matches lines with answer choices, formatted as a letter (A-D) followed by a parenthesis, and the answer text.
   - Captures the answer letter and text.

3. `correct_answer_pattern = r"^\s+\*\*Answer:\s+([A-D])\)\s+(.+)$"`:
   - Matches lines indicating the correct answer, starting with "**Answer:**".
   - Captures the correct answer letter.

## Usage

Run the script using the following command:

```bash
python process3.py "filename.md" [--convert]
```

- Replace `"filename.md"` with the path to your Markdown file.
- Use the `--convert` flag to automatically run `text2qti` on the generated file.

## Installation Requirements

- Python 3
- `text2qti` package (for the `--convert` option)

Install `text2qti` using pip:

```bash
python -m pip install text2qti
```

## Script API

The script defines several functions:

- `convert_md_to_text2qti(md_content)`: Converts Markdown content to text2qti format.
- `read_and_convert_file(file_name)`: Reads the specified Markdown file and returns the converted content.
- `run_text2qti(output_file)`: Runs the `text2qti` command on the given file (used when `--convert` flag is present).

---

This README provides an overview of the script's functionality, its regular expressions, and usage instructions. You can place this in your GitHub repository to serve as documentation for users who want to understand and use your script.
