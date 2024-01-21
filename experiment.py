import os
import PyPDF2
import openai
from dotenv import load_dotenv
# Function to analyze the directory
def analyze_directory(directory):
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

# Function to read file content
def read_file_content(file_info):
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

# Function to get file contents
def get_file_contents(file_details):
    content_details = []
    for file_info in file_details:
        try:
            file_content = read_file_content(file_info)
            print(len(file_content.split()))
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
    :return: A summary of the text within the specified word range if word count exceeds GLOBAL_TOKEN_SIZE.
    """
    global_token_size = int(os.getenv('GLOBAL_TOKEN_SIZE'))
    word_count = len(text.split())

    if word_count > global_token_size:
        client = openai.OpenAI(api_key=api_key)
        prompt = f"You are a professor that needs to reduce the size of a large text without losing information on the important topics covered in a text. Summarize the following text to a summary between {min_words} and {max_words} words:\n\n{text}"

        while True:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                max_tokens=250,  # Adjust as needed
                stop=None,
                temperature=0.7
            )

            summary = response.choices[0].message.content.strip()
            summary_word_count = len(summary.split())

            if min_words <= summary_word_count <= max_words:
                break

        return summary





# Main execution
if __name__ == "__main__":
    load_dotenv()
    directory_path = "C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI"
    api_key = os.getenv('OPENAI_API_KEY')  # Set this in your environment variables
    print(api_key)
    min_words = 50  # Adjust as needed
    max_words = 100  # Adjust as needed

    file_details = analyze_directory(directory_path)
    file_contents = get_file_contents(file_details)
    for file in file_contents:
        summarized_content = summarize_text(api_key, file['content'], min_words, max_words)
        print(f"File: {file['path']}\nContent: {summarized_content}\n")
