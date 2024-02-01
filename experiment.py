import os
import PyPDF2
import openai
import tiktoken
from dotenv import load_dotenv
import logging

# Configure basic logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_directory(directory):
    """
    Analyzes the content of the given directory and returns details of specific file types.
    This version only checks the current directory and does not descend into child directories.

    :param directory: The path of the directory to analyze.
    :return: A list of dictionaries, each containing 'name', 'type', 'size', and 'path' of the file.
    """
    logging.info(f"Analyzing directory: {directory}")
    supported_extensions = {'.md', '.ipynb', '.py', '.pdf'}
    file_details = []

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Check if it's a file
            extension = os.path.splitext(file_path)[1]
            if extension in supported_extensions:
                file_info = {
                    'name': file,
                    'type': extension,
                    'size': os.path.getsize(file_path),
                    'path': file_path
                }
                file_details.append(file_info)
                logging.info(f"File added for processing: {file_path}")

    return file_details

def read_file_content(file_info):
    """
    Reads the content of a file based on its type and returns the content as a string.

    :param file_info: Dictionary containing the file's details.
    :return: Content of the file as a string.
    """
    file_path = file_info['path']
    file_type = file_info['type']
    content = ''

    try:
        if file_type == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content += page.extract_text()
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

        logging.info(f"Successfully read content from: {file_path}")
    except Exception as e:
        logging.exception(f"Error reading {file_path}: {e}")

    return content

def get_file_contents(file_details):
    """
    Retrieves the contents of each file based on the provided file details.

    :param file_details: List of dictionaries containing file details.
    :return: A list of dictionaries, each containing 'path' and 'content' of the file.
    """
    content_details = []
    for file_info in file_details:
        file_content = read_file_content(file_info)
        if file_content:
            content_details.append({
                'path': file_info['path'],
                'content': file_content
            })

    return content_details

def summarize_files(api_key, file_details, min_words, max_words):
    """
    Summarizes the content of files whose content exceeds a specified global token size. 
    The function processes a list of file details, checks the token size of each file's content, 
    and if it exceeds the global token size limit, it uses the OpenAI API to generate a summary. 
    The summary process continues until the word count of the summary falls within the specified 
    minimum and maximum word range. The function returns a list of dictionaries with the filename/path, 
    file content (original or summarized), and the token size of the content.

    :param api_key: Your OpenAI API key.
    :param file_details: List of dictionaries with file details.
    :param min_words: The minimum word count of the summary.
    :param max_words: The maximum word count of the summary.
    :return: A list of dictionaries with filename/path, file content, and token size.
    """
    global_token_size = int(os.getenv('GLOBAL_TOKEN_SIZE'))
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
    summarized_files = []

    for file in file_details:
        original_token_count = len(encoding.encode(file['content']))

        if original_token_count > global_token_size:
            client = openai.OpenAI(api_key=api_key)
            prompt_system = "You are a professor developing content for a course in business analytics. You will be provided with text content. Summarize the content without losing information on the important topics covered in the text."
            prompt_user = f"Summarize the text delimited by triple quotes between {min_words} and {max_words} words.'''{file['content']}'''"
            summary = ''
            while True:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_user}
                    ],
                    max_tokens=250,
                    stop=None,
                    temperature=0.7
                )
                summary = response.choices[0].message.content.strip()
                word_count = len(summary.split())

                if min_words <= word_count <= max_words:
                    break

            file_content = summary
            token_count = len(encoding.encode(summary))
        else:
            file_content = file['content']
            token_count = original_token_count

        summarized_files.append({
            'path': file['path'],
            'content': file_content,
            'token_size': token_count
        })

    return summarized_files

# Main execution
if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()

    # Define the path of the directory to analyze
    directory_path = "C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI"

    # Retrieve the OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')

    # Set the minimum and maximum word limits for the summaries
    min_words = 50
    max_words = 100

    try:
        # Analyze the directory and get details of the files present
        file_details = analyze_directory(directory_path)

        # Retrieve the contents of each file from the analyzed directory
        file_contents = get_file_contents(file_details)

        # Summarize the content of the files using the OpenAI API
        summarized_contents = summarize_files(api_key, file_contents, min_words, max_words)

        # Log the information about the files and their summarized content if it's within the specified word range
        for file in summarized_contents:
            word_count = len(file['content'].split())
            if min_words <= word_count <= max_words:
                logging.info(f"File summarized: {file['path']}\nContent: {file['content']}\nToken_count:{file['token_size']}")

    # Catch and log any exceptions that occur during the execution
    except Exception as e:
        logging.exception(f"An error occurred during execution: {e}")

