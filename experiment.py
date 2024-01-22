import os
import PyPDF2
import openai
import tiktoken
from dotenv import load_dotenv
# Function to analyze the directory

import logging

# Configure basic logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_directory(directory):
    """
    Analyzes the content of the given directory and returns details of specific file types.

    :param directory: The path of the directory to analyze.
    :return: A list of dictionaries, each containing 'name', 'type', 'size', and 'path' of the file.
    """
    supported_extensions = {'.md', '.ipynb', '.py', '.pdf'}
    file_details = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file_path)[1]

            if extension in supported_extensions:
                file_info = {
                    'name': file,
                    'type': extension,
                    'size': os.path.getsize(file_path),
                    'path': file_path
                }
                file_details.append(file_info)

    return file_details


def read_file_content(file_info):
    """
    Reads the content of a file based on its type.

    :param file_info: Dictionary containing 'name', 'type', 'size', and 'path' of the file.
    :return: The content of the file as a string.
    """
    file_path = file_info['path']
    file_type = file_info['type']

    if file_type == '.pdf':
        content = ''
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                content += page.extract_text()
        return content

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_file_contents(file_details):
    """
    Gets the contents of files based on the details provided.

    :param file_details: List of dictionaries containing file details.
    :return: A list of dictionaries, each containing 'path' and 'content' of the file.
    """
    content_details = []
    for file_info in file_details:
        try:
            file_content = read_file_content(file_info)
            content_details.append({
                'path': file_info['path'],
                'content': file_content
            })
        except Exception as e:
            print(f"Error reading {file_info['path']}: {e}")
   
    return content_details


def summarize_text(api_key, text, min_words, max_words):
    """
    Summarize the provided text to a summary between min_words and max_words in length if it exceeds the GLOBAL_TOKEN_SIZE.

    :param api_key: Your OpenAI API key.
    :param text: The text to summarize.
    :param min_words: The minimum word count of the summary.
    :param max_words: The maximum word count of the summary.
    :return: A summary of the text within the specified word range if token count exceeds GLOBAL_TOKEN_SIZE.
    """
    global_token_size = int(os.getenv('GLOBAL_TOKEN_SIZE'))
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    token_count = len(encoding.encode(text))
   
    if token_count > global_token_size:
        client = openai.OpenAI(api_key=api_key)
        
        # System prompt with context as a professor developing content for business analytics
        prompt_system = "You are a professor developing content for a course in business analytics. You will be provided with a text content. Summarize the content without losing information on the important topics covered in the text."

        # User prompt asking to summarize the text within a specified word range
        prompt_user = f"Summarize the text delimited by triple quotes between {min_words} and {max_words} words.'''{text}'''"

        while True:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": prompt_user}
                ],
                max_tokens=250,  # Adjust as needed
                stop=None,
                temperature=0.7
            )

            summary = response.choices[0].message.content.strip()
            summary_word_count = len(summary.split())
            print(summary_word_count)
            if min_words <= summary_word_count <= max_words:
                break

        return summary
    else:
        return None

# Main execution
if __name__ == "__main__":
    # Load environment variables from a .env file
    load_dotenv()

    # Specify the directory path to analyze
    directory_path = "C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI"

    # Retrieve the OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')

    # Define the minimum and maximum word count for summaries
    min_words = 50
    max_words = 100

    # Analyze the specified directory and get file details
    # This includes the name, type, size, and path of each file
    file_details = analyze_directory(directory_path)

    # Read the contents of each file found in the directory
    file_contents = get_file_contents(file_details)

    # Iterate through each file's contents
    for file in file_contents:
        # Summarize the content of the file if it exceeds the global token size limit
        summarized_content = summarize_text(api_key, file['content'], min_words, max_words)

        # Print the path of the file and its summarized content
        # If the content is not summarized (below token limit), it prints 'None'
        print(f"File: {file['path']}\nContent: {summarized_content}\n")

