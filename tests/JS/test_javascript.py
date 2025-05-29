''' This file helps check the Javascript files for syntax or other errors. 
It uses the Node.js command line tool to check the syntax of each .js file in the specified directory. 
If any errors are found, it prints them to the console.
'''

import unittest
import os
import subprocess
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
JS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'js'))

NODE_PATH = r"C:\<your_node_path>\nodejs\node.exe"

class TestJSValidation(unittest.TestCase):

    def test_js_syntax(self):
        all_passed = True  # Flag to track overall test result

        print("\nJS Validation Report\n" + "-" * 30)

        for root, _, files in os.walk(JS_DIR):
            for file in files:
                if file.endswith(".js"):
                    filepath = os.path.join(root, file)
                    result = subprocess.run([NODE_PATH, '--check', filepath], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"{file}: PASSED (No syntax errors)")
                    else:
                        print(f"{file}: FAILED (Syntax errors)\n{result.stderr}")
                        all_passed = False

        if all_passed:
            print("\nOverall Result: All JS files passed validation.\n\n")
        else:
            print("\nOverall Result: Some JS files failed validation.\n\n")

if __name__ == '__main__':
    unittest.main()
