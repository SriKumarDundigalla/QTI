# Markdown to QTI Converter Application

## Overview
This application converts Markdown files containing questions and learning outcomes into QTI (Question and Test Interoperability) format. It's designed for users who wish to create quizzes for learning platforms from Markdown-formatted text.

## How to Use

### Prerequisites for Successful Conversion

**Note: It is essential to format your Markdown file correctly for the application to work as intended.**

- **Proper Markdown Formatting**: Your Markdown file must be structured in a specific way, particularly for quizzes and learning outcomes. The application relies on this format to accurately convert the content into QTI format.

- **Example Files for Reference**: Please refer to the provided examples ([mapreduce_test2.md](https://github.com/SriKumarDundigalla/QTI/blob/main/mapreduce_test2.md) or [mongo_test1.md](https://github.com/SriKumarDundigalla/QTI/blob/main/mongo_test1.md)) as a template. These files demonstrate the necessary structure, especially how to map questions in the learning outcomes table.

- **Mandatory Learning Outcomes Mapping**: Ensure that your quiz questions are correctly mapped to the respective learning outcomes in your Markdown file, similar to the structure used in the example files. This mapping is crucial for the application to accurately organize and convert the quiz content.

### Steps for Usage
1. **Place Files in Same Folder**: Put `application.exe` and your Markdown file in the same directory.

2. **Run the Executable**: Double-click `application.exe` to run the application.

3. **Input Markdown Filename**: When prompted, enter the name of your Markdown file, including the `.md` extension.

4. **Input Prefix for QTI Files**: Next, enter a prefix for the QTI files. This prefix will precede the names of the output QTI files.

5. **Upload to Learning Platform**: The application generates QTI files in a zip format, which you can upload to various learning platforms. This allows you to create quizzes and save them to question banks.

6. **Output Files**: All these files are neatly organized in an output folder created by the application. Inside this folder, you'll find two subfolders:
   - **Text Files**: Contains all the quiz files in plain text format.
   - **QTI Files**: Contains the QTI formatted files, ready to be uploaded to your learning management system.

### Technical Details
- This application is developed in Python 3 and uses libraries such as `re` (for regular expressions), `subprocess`, and `os`.
- To convert the Python script into an executable file, `pyinstaller` was utilized.

## Installation Requirements
- No additional installation is required for running `application.exe`.
- For Markdown file preparation, any text editor capable of saving files in Markdown format will suffice. Some popular options include [Visual Studio Code](https://code.visualstudio.com/), [Atom](https://atom.io/), [Sublime Text](https://www.sublimetext.com/), [Notepad++](https://notepad-plus-plus.org/), and [MarkdownPad](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

## Support
If you encounter any issues or have questions about using the application, please feel free to contact [srikumar@usf.edu](mailto:srikumar@usf.edu)



