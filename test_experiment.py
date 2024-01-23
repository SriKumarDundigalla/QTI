import unittest
import os
import experiment  # Replace with the actual name if different

class TestExperiment(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment before each test.

        This method creates a test directory and populates it with a test markdown file and another file
        of a type that should be ignored by the analyze_directory function.
        """
        self.test_dir = 'test_directory'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'test.md'), 'w') as f:
            f.write('Markdown content')
        with open(os.path.join(self.test_dir, 'ignore.txt'), 'w') as f:
            f.write('This should be ignored')

    def test_analyze_directory(self):
        """
        Test the analyze_directory function to ensure it correctly identifies and lists supported file types.

        This test verifies that the function correctly includes files with supported extensions in its results
        and excludes files with unsupported extensions.
        """
        result = experiment.analyze_directory(self.test_dir)
        expected_files = ['test.md']
        found_files = [file_detail['name'] for file_detail in result]
        self.assertListEqual(found_files, expected_files)

    def test_read_file_content(self):
        """
        Test the read_file_content function to ensure it correctly reads the content from a file.

        This test checks if the function correctly reads and returns the content of a markdown file.
        It also validates that the function is provided with the correct file information, including the file type.
        """
        file_info = {'path': os.path.join(self.test_dir, 'test.md'), 'type': '.md'}
        content = experiment.read_file_content(file_info)
        self.assertEqual(content, 'Markdown content')

    def tearDown(self):
        """
        Clean up the test environment after each test.

        This method removes the created test directory and all of its contents, ensuring a clean state for the next test.
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()
