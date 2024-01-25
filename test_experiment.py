import unittest
import os
from unittest.mock import patch
import experiment 
import HtmlTestRunner

class TestExperiment(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)

        with open(os.path.join(self.test_dir, 'test.md'), 'w') as f:
            f.write('Markdown content')

        with open(os.path.join(self.test_dir, 'ignore.txt'), 'w') as f:
            f.write('This should be ignored')

        self.test_file_path = os.path.join(self.test_dir, 'test_small_file.md')
        with open(self.test_file_path, 'w') as f:
            f.write('Small file content' * 100)  # Adjust the multiplier to ensure content is less than 8000 tokens

    def test_analyze_directory(self):
        """
        Test the analyze_directory function to ensure it correctly identifies and lists supported file types.
        """
        result = experiment.analyze_directory(self.test_dir)
        expected_files = ['test.md', 'test_small_file.md']
        found_files = [file_detail['name'] for file_detail in result]
        self.assertListEqual(sorted(found_files), sorted(expected_files))

    def test_read_file_content(self):
        """
        Test the read_file_content function to ensure it correctly reads the content from a file.
        """
        file_info = {'path': os.path.join(self.test_dir, 'test.md'), 'type': '.md'}
        content = experiment.read_file_content(file_info)
        self.assertEqual(content, 'Markdown content')

    @patch.dict(os.environ, {'GLOBAL_TOKEN_SIZE': '8000', 'OPENAI_API_KEY': 'fake_api_key'})
    def test_summarize_files_with_small_content(self):
        """
        Test the summarize_files function to ensure it returns original content for files with less than 8000 tokens.
        """
        file_details = [{'path': self.test_file_path, 'type': '.md', 'content': 'Small file content' * 100}]
        summarized_contents = experiment.summarize_files('fake_api_key', file_details, 50, 100)

        for file in summarized_contents:
            self.assertEqual(file['content'], 'Small file content' * 100)
       

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='C:/Users/dsksr/Documents/BIG DATA/2024/QTI/GIT/QTI-AI/QTI'))

