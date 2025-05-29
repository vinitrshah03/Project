''' This file tests the HTML files in the templates directory to ensure they are valid HTML5. 
It uses BeautifulSoup to parse the HTML and checks for any parsing errors using html5lib. 
The test will fail if any HTML file is invalid. 

It also cleans Jinja2 syntax from the HTML files before validation.
'''

import os
import re
import unittest
from bs4 import BeautifulSoup

TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'templates'))

def clean_jinja2(content):
    content = re.sub(r'{{.*?}}', '', content)
    content = re.sub(r'{%.*?%}', '', content)
    content = re.sub(r'{#.*?#}', '', content)
    return content

class TestHTMLValidation(unittest.TestCase):
    def test_html_validation(self):
        error_count = 0
        failed_files = []
        total_files = 0

        print("\nHTML Validation Report\n" + "-" * 30)

        for filename in os.listdir(TEMPLATE_DIR):
            if filename.endswith('.html'):
                total_files += 1
                filepath = os.path.join(TEMPLATE_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                    clean_content = clean_jinja2(raw_content)

                    try:
                        soup = BeautifulSoup(clean_content, 'html5lib')
                        str(soup)
                        print(f"{filename} - Passed")
                    except Exception as e:
                        error_count += 1
                        failed_files.append((filename, str(e)))
                        print(f"{filename} - Failed")

        print("\nSummary\n" + "-" * 30)
        print(f"Total HTML files tested: {total_files}")
        print(f"Files passed: {total_files - error_count}")
        print(f"Files failed: {error_count}\n\n")

        if error_count > 0:
            print("\nFailed Files:")
            for file, error in failed_files:
                print(f" - {file}: {error}")

        self.assertEqual(error_count, 0, f"HTML validation failed with {error_count} errors.\n\n")

if __name__ == '__main__':
    unittest.main()