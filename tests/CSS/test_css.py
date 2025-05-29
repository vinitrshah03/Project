''' This file helps to validate CSS files in the templates directory. '''

import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
CSS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'css'))

class TestCSSValidation(unittest.TestCase):

    def test_css_files(self):
        all_passed = True  # Flag to track overall test result

        print("\nCSS Validation Report\n" + "-" * 30)

        for root, _, files in os.walk(CSS_DIR):
            for file in files:
                if file.endswith(".css"):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                            if ';;' in content:
                                print(f"{file}: FAILED (contains double semicolons)")
                                all_passed = False
                            else:
                                print(f"{file}: PASSED")
                    except Exception as e:
                        print(f"Error reading {file}: {str(e)}")
                        all_passed = False

        if all_passed:
            print("\nOverall Result: All CSS files passed validation.\n\n")
        else:
            print("\nOverall Result: Some CSS files failed validation.\n\n")

if __name__ == '__main__':
    unittest.main()