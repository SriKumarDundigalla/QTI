import os
import PyPDF2
import tiktoken
import openai
from dotenv import load_dotenv
load_dotenv() 
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
            content_details.append({
                'path': file_info['path'],
                'content': file_content
            })
        except Exception as e:
            print(f"Error reading {file_info['path']}: {e}")

    return content_details

# Function to summarize large files
def summarize_large_files(filepath, content):
    global_token_size = int(os.getenv('GLOBAL_TOKEN_SIZE'))

    # Count tokens
    encoding = tiktoken.encoding_for_model("gpt-4-1106-preview")
    token_count = len(encoding.encode(content))

    if token_count > global_token_size:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are an assistant who summarizes long documents."},
                {"role": "user", "content": f"Please summarize the following content:\n{content}"}
            ]
        )
        return response.choices[0].message['content']
    else:
        return content

# Main execution
if __name__ == "__main__":
    directory_path = "C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI"
    file_details = analyze_directory(directory_path)
    file_contents = get_file_contents(file_details)

    for file in file_contents:
        summarized_content = summarize_large_files(file['path'], file['content'])
        print(f"File: {file['path']}\nContent: {summarized_content}\n")
