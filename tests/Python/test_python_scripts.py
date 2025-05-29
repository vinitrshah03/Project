import unittest
import importlib
import traceback
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
MODULES_TO_TEST = ['app', 'recommender', 'config', 'keylogger']

class ModuleImportTest(unittest.TestCase):

    test_results = {}

    def test_imports(self):
        print("\nPython Validation Report\n" + "-" * 30)

        for module_name in MODULES_TO_TEST:
            try:
                print(f"\n[Testing: {module_name}.py]")
                importlib.import_module(module_name)
                self.test_results[module_name] = "OK"
                print(f"{module_name}: OK")
            except SystemExit:
                self.test_results[module_name] = "STOP (SystemExit)"
                print(f"{module_name}: STOP (SystemExit)")
            except Exception as e:
                self.test_results[module_name] = f"ERROR - {str(e)}"
                print(f"{module_name}: ERROR - {str(e)}")
                traceback.print_exc()

        # Print the overall test results
        print("\nOverall Test Results:\n" + "-" * 30)
        for module_name, result in self.test_results.items():
            print(f"{module_name}.py: {result}")

if __name__ == "__main__":
    unittest.main()