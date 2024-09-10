import subprocess
import os

class TestRunner:
    def run_tests(self, tests, code):
        # Save the code to a temporary file
        with open("temp_code.py", "w") as f:
            f.write(code)

        # Create a test file
        with open("test_code.py", "w") as f:
            f.write("import unittest\n")
            f.write("from temp_code import *\n\n")
            f.write("class TestCode(unittest.TestCase):\n")
            for i, test in enumerate(tests):
                f.write(f"    def test_{i}(self):\n")
                f.write(f"        {test}\n\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    unittest.main()")

        # Run the tests
        result = subprocess.run(["python", "test_code.py"], capture_output=True, text=True)

        # Parse the test results
        test_results = []
        for line in result.stdout.split("\n"):
            if line.startswith("test_"):
                test_results.append("ok" in line.lower())

        # Clean up temporary files
        os.remove("temp_code.py")
        os.remove("test_code.py")

        return test_results