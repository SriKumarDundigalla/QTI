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

--------------------------------------------------------------------------------------------------------------------

# text2qti api

`text2qti` is a Python package that converts text files into quizzes in QTI (Question and Test Interoperability) format. It's particularly useful for creating quizzes that can be imported into learning management systems like Canvas. Here's a detailed overview of the different types of questions you can create with `text2qti` and their explanations:

### 1. Multiple-Choice Questions
- **Syntax**: Questions are numbered and followed by possible answers, which are labeled with lowercase letters followed by a parenthesis. The correct answer is marked with an asterisk (`*`).
- **Example**:
  ```
  1. What is the capital of France?
  a) Berlin
  b) Madrid
  *c) Paris
  ```

### 2. Multiple-Answers Questions
- **Syntax**: Similar to multiple-choice, but more than one answer can be correct. Incorrect answers are marked with `[]`, and correct answers with `[*]`.
- **Example**:
  ```
  1. Which of the following are European countries?
  [*] Germany
  [ ] Brazil
  [*] Italy
  [ ] Canada
  ```

### 3. True/False Questions
- **Syntax**: These are a simple form of multiple-choice questions with only two options, true and false.
- **Example**:
  ```
  1. The Earth is flat.
  *a) False
  b) True
  ```

### 4. Short-Answer (Fill-in-the-Blank) Questions
- **Syntax**: The answer is preceded by an asterisk and space. Multiple acceptable answers can be provided.
- **Example**:
  ```
  1. Who wrote "To Kill a Mockingbird"?
  * Harper Lee
  ```

### 5. Essay Questions
- **Syntax**: Indicated by a sequence of three or more underscores. They typically support general question feedback but not specific answers.
- **Example**:
  ```
  1. Discuss the impact of globalization.
  ___
  ```

### 6. Numerical Questions
- **Syntax**: Use an equals sign followed by the numerical answer. You can specify a range or an exact answer with a margin of error.
- **Example**:
  ```
  1. What is the value of Pi (up to 2 decimal places)?
  = 3.14 +- 0.01
  ```

### 7. File-Upload Questions
- **Syntax**: Indicated by a sequence of three or more circumflex accents. Like essay questions, they mainly support general feedback.
- **Example**:
  ```
  1. Upload a file containing your project proposal.
  ^^^^
  ```

### 8. Text Regions
- **Syntax**: Not a question type but allows you to include additional text sections within a quiz.
- **Example**:
  ```
  Text: Please read the following instructions carefully before proceeding.
  ```

### Additional Features
- **Question Groups**: Randomly selects a specified number of questions from a set.
- **Executable Code Blocks**: Executes Python code to dynamically generate questions.
- **Quiz Options**: Settings for answer shuffling, showing correct answers, etc.
- Markdown syntax is heavily used for formatting text, so familiarity with Markdown is beneficial.
- The package is designed with Canvas LMS in mind, but the generated QTI files might work with other systems that support QTI.

### Installation
`text2qti` can be installed via pip:
```bash
python -m pip install text2qti
```
