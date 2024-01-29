import unittest
import os
from unittest.mock import patch, MagicMock
import experiment
import HtmlTestRunner

class TestExperiment(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test. This includes creating a test directory and populating it with
        different types of files - a markdown file (test.md), a file to be ignored (ignore.txt), a small file for testing
        token limits (test_small_file.md), and a large file to test API summarization (large_file.md).
        """
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

        with open(os.path.join(self.test_dir, 'test.md'), 'w') as f:
            f.write('Markdown content')

        with open(os.path.join(self.test_dir, 'ignore.txt'), 'w') as f:
            f.write('This should be ignored')

        self.test_file_path = os.path.join(self.test_dir, 'test_small_file.md')
        with open(self.test_file_path, 'w') as f:
            f.write('Small file content' * 100)

        self.large_file_path = os.path.join(self.test_dir, 'large_file.md')
        with open(self.large_file_path, 'w') as f:
            f.write('Large file content' * 8000)

    def test_analyze_directory(self):
        """
        Test the analyze_directory function to verify it correctly identifies and lists supported file types.
        This function should only include files with specific extensions and exclude others.
        """
        result = experiment.analyze_directory(self.test_dir)
        expected_files = ['test.md', 'test_small_file.md', 'large_file.md']
        found_files = [file_detail['name'] for file_detail in result]
        self.assertListEqual(sorted(found_files), sorted(expected_files))

    def test_read_file_content(self):
        """
        Test the read_file_content function to ensure it correctly reads and returns the content of a file.
        This test is specifically checking the ability to read the contents of a markdown file.
        """
        file_info = {'path': os.path.join(self.test_dir, 'test.md'), 'type': '.md'}
        content = experiment.read_file_content(file_info)
        self.assertEqual(content, 'Markdown content')

    @patch.dict(os.environ, {'GLOBAL_TOKEN_SIZE': '8000', 'OPENAI_API_KEY': 'fake_api_key'})
    def test_summarize_files_with_small_content(self):
        """
        Test the summarize_files function to confirm that it returns the original content for files with less than 8000 tokens.
        This test checks the function's ability to handle small files that don't require summarization.
        """
        file_details = [{'path': self.test_file_path, 'type': '.md', 'content': 'Small file content' * 100}]
        summarized_contents = experiment.summarize_files('fake_api_key', file_details, 50, 100)

        for file in summarized_contents:
            self.assertEqual(file['content'], 'Small file content' * 100)

    @patch.dict(os.environ, {'GLOBAL_TOKEN_SIZE': '8000', 'OPENAI_API_KEY': 'fake_api_key'})
    @patch('experiment.openai.OpenAI')
    def test_summarize_files_with_large_content(self, mock_openai_class):
        """
        Test the summarize_files function to ensure it returns a summary for files with content greater than 8000 tokens.
        This test mocks the OpenAI API call and verifies that the function returns the mock summary for large files.
        """
        # Mock setup for OpenAI API response
        mock_summary = ' '.join(['Mocked summary content.'] * 50)
        mock_choice = MagicMock()
        mock_choice.message.content = mock_summary
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        # Mock OpenAI API client
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        file_details = [{'path': self.large_file_path, 'type': '.md', 'content': 'Large file content' * 8000}]
        summarized_contents = experiment.summarize_files('fake_api_key', file_details, 50, 100)

        for file in summarized_contents:
            self.assertEqual(file['content'], mock_summary)

    def tearDown(self):
        """
        Clean up the test environment after each test. This involves removing the created test directory and all its contents.
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI'))
