import os
import PyPDF2
import openai
import tiktoken
from dotenv import load_dotenv
import logging
# Load environment variables from the .env file
load_dotenv()
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
                word_count = len(encoding.encode(summary))

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

def create_chunks_from_content(file_contents, context_window_size ):
    """
    Creates content chunks from a list of file content dictionaries, ensuring that each chunk does not exceed a specified context window size in terms of tokens.

    The function sorts the file contents by their token size in descending order to start chunk creation with the largest content first. It then iteratively adds content to a chunk until the context window size is reached or exceeded. Once a chunk reaches this limit, it's added to the list of all chunks, and the process continues with the creation of a new chunk. The function ensures that all content is used, dividing it into as few chunks as possible without exceeding the specified token limit for each chunk.

    Parameters:
    - file_contents (list of dict): A list of dictionaries, where each dictionary contains 'content' (str) and 'token_size' (int) keys. 'content' is the text of the file, and 'token_size' is the number of tokens that text consists of.
    - context_window_size (int): The maximum number of tokens that a single chunk can contain. It defines the upper limit for the size of each content chunk.

    Returns:
    - list of str: A list of content chunks, where each chunk is a string composed of file contents that together do not exceed the context window size.

    The function prioritizes larger contents for earlier chunks by sorting the input based on token size in descending order. It tracks which contents have been used to ensure that all content is accounted for and to prevent any single content from being used in multiple chunks. If a piece of content is too large to fit into the current chunk without exceeding the context window, it starts a new chunk with that content. The process repeats until all contents have been assigned to a chunk, ensuring efficient use of the context window size.
    """
    # Initialize the list to hold all content chunks
    all_chunks = []
    # Sort file_contents by 'token_size' in descending order
    sorted_file_contents = sorted(file_contents, key=lambda x: x['token_size'], reverse=True)
    # Track indices of contents that have been used
    used_indices = set()

    # Outer Loop: Continue until all content has been used
    while len(used_indices) < len(sorted_file_contents):
        current_chunk = ""
        current_token_count = 0
        # Iterate over sorted_file_contents to try fitting content into the current chunk
        for i, file_content in enumerate(sorted_file_contents):
            if i in used_indices:
                continue  # Skip content that's already been used
            content = file_content['content']
            token_size = file_content['token_size']
            # Check if adding this content exceeds the context window size
            if current_token_count + token_size <= context_window_size:
                current_chunk += content  # Add content to the current chunk
                current_token_count += token_size
                used_indices.add(i)  # Mark this content as used

        # After trying to add all possible content to the current chunk
        if current_chunk:  # If the current chunk contains any content, add it to all_chunks
            all_chunks.append(current_chunk)
        else:
            # If no content could be added (due to all remaining contents being too large),
            # break the loop to prevent an infinite loop
            break

    return all_chunks




# Main execution
if __name__ == "__main__":
    # Load environment variables from the .env file
    load_dotenv()

    # Define the path of the directory to analyze
    directory_path = r"C:\Users\dsksr\Documents\BIG DATA\2024\Independent Study\QTI\GIT\Dev-ai\QTI"

    # Retrieve the OpenAI API key from environment variables
    api_key = os.getenv('OPENAI_API_KEY')
    context_window_size =int(os.getenv('context_window_size'))
    # Set the minimum and maximum word limits for the summaries
    min_words = 50
    max_words = 100

    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-1106")

    try:
        # Analyze the directory and get details of the files present
        file_details = analyze_directory(directory_path)
        
        # Retrieve the contents of each file from the analyzed directory
        file_contents = get_file_contents(file_details)

        # Summarize the content of the files using the OpenAI API
        summarized_contents = summarize_files(api_key, file_contents, min_words, max_words)

        chunked_contents = create_chunks_from_content(summarized_contents,context_window_size)
        for i in chunked_contents:
            print(len(encoding.encode(i)))

    # Catch and log any exceptions that occur during the execution
    except Exception as e:
        logging.exception(f"An error occurred during execution: {e}")

