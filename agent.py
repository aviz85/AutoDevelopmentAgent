import anthropic
import json
import logging
from test_runner import TestRunner
from feature_developer import FeatureDeveloper

class AutoDevelopmentAgent:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.test_runner = TestRunner()
        self.feature_developer = FeatureDeveloper(api_key)

    def process_user_idea(self, idea):
        logging.info("Starting to process user idea")
        
        # Step 1: Create specification and user stories
        logging.info("Creating specification")
        specification = self.create_specification(idea)

        # Step 2: Plan tests
        logging.info("Planning tests")
        tests = self.plan_tests(specification)

        # Step 3: Develop features
        logging.info("Developing features")
        code = self.develop_features(specification)

        # Step 4: Run tests
        logging.info("Running tests")
        test_results = self.run_tests(tests, code)

        # Step 5: Improve code
        iteration = 0
        max_iterations = 5
        while not all(test_results) and iteration < max_iterations:
            logging.info(f"Improving code - Iteration {iteration + 1}")
            code = self.improve_code(code, test_results)
            test_results = self.run_tests(tests, code)
            iteration += 1

        logging.info("Finished processing user idea")
        return code

    def create_specification(self, idea):
        prompt = f"Create a specification including user stories for the following idea: {idea}"
        response = self.client.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=1000,
            prompt=prompt
        )
        return response.completion

    def plan_tests(self, specification):
        prompt = f"Plan tests for the user experience based on this specification: {specification}"
        response = self.client.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=1000,
            prompt=prompt
        )
        return json.loads(response.completion)

    def develop_features(self, specification):
        return self.feature_developer.develop(specification)

    def run_tests(self, tests, code):
        return self.test_runner.run_tests(tests, code)

    def improve_code(self, code, test_results):
        prompt = f"Improve this code to pass all tests:\n{code}\nTest results: {test_results}"
        response = self.client.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=2000,
            prompt=prompt
        )
        return response.completion

# Remove the usage example from here as it's not needed in the class file