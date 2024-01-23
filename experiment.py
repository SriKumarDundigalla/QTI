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

    :param directory: The path of the directory to analyze.
    :return: A list of dictionaries, each containing 'name', 'type', 'size', and 'path' of the file.
    """
    logging.info(f"Analyzing directory: {directory}")
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
    Processes a list of file details and returns a data structure with filename/path and file content.
    Files with content that exceeds the specified token size are summarized using the ChatGPT API.

    :param api_key: Your OpenAI API key.
    :param file_details: List of dictionaries with file details.
    :param min_words: The minimum word count of the summary.
    :param max_words: The maximum word count of the summary.
    :return: A list of dictionaries with filename/path and file content.
    """
    global_token_size = int(os.getenv('GLOBAL_TOKEN_SIZE'))
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")
    summarized_files = []

    for file in file_details:
        token_count = len(encoding.encode(file['content']))

        if token_count > global_token_size:
            client = openai.OpenAI(api_key=api_key)
            prompt_system = "You are a professor developing content for a course in business analytics. You will be provided with text content. Summarize the content without losing information on the important topics covered in the text."
            prompt_user = f"Summarize the text delimited by triple quotes between {min_words} and {max_words} words.'''{file['content']}'''"

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
            file_content = summary
        else:
            file_content = file['content']
            print(file_content)

        summarized_files.append({'path': file['path'], 'content': file_content})

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

        # Log the information about the files and their summarized content
        for file in summarized_contents:
            logging.info(f"File summarized: {file['path']}\nContent: {file['content']}\n")

    # Catch and log any exceptions that occur during the execution
    except Exception as e:
        logging.exception(f"An error occurred during execution: {e}")

