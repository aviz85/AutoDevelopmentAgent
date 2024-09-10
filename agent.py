import anthropic
import json
import logging
import os
import re
from dotenv import load_dotenv
from test_runner import TestRunner
from feature_developer import FeatureDeveloper

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutoDevelopmentAgent:
    def __init__(self, max_tokens=None):
        load_dotenv()
        self.client = anthropic.Anthropic()
        logging.info("Anthropic client initialized successfully")
        self.test_runner = TestRunner()
        self.feature_developer = FeatureDeveloper(max_tokens)
        self.max_tokens = max_tokens
        self.total_tokens_used = 0

    def process_user_idea(self, idea):
        # This method is now only used for the CLI version
        logging.info("Starting to process user idea")
        specification = self.create_specification(idea)
        tests = self.plan_tests(specification)
        code = self.develop_features(specification)
        test_results = self.run_tests(tests, code)
        
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
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=min(1000, self.max_tokens) if self.max_tokens else 1000,
                messages=[
                    {"role": "user", "content": f"Create a specification including user stories for the following idea: {idea}. Provide the output as plain text without any markdown formatting."}
                ]
            )
            self.total_tokens_used += message.usage.output_tokens
            logging.info(f"Tokens used in create_specification: {message.usage.output_tokens}")
            return self.remove_markdown(message.content[0].text)
        except Exception as e:
            logging.error(f"Error in create_specification: {str(e)}")
            raise

    def plan_tests(self, specification):
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=min(1000, self.max_tokens) if self.max_tokens else 1000,
                messages=[
                    {"role": "user", "content": f"Plan tests for the user experience based on this specification: {specification}\n\nProvide the test plan as a valid JSON array of test objects. Each test object should have 'name' and 'steps' fields."}
                ]
            )
            self.total_tokens_used += message.usage.output_tokens
            logging.info(f"Tokens used in plan_tests: {message.usage.output_tokens}")
            response_text = message.content[0].text
            logging.info(f"Raw response from API: {response_text}")
            
            # Try to extract JSON from the response
            try:
                json_start = response_text.index('[')
                json_end = response_text.rindex(']') + 1
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            except ValueError:
                logging.error(f"Could not find valid JSON in the response: {response_text}")
                return []  # Return an empty list if no valid JSON is found
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON in plan_tests: {str(e)}")
            logging.error(f"Response content: {response_text}")
            return []  # Return an empty list if JSON decoding fails
        except Exception as e:
            logging.error(f"Error in plan_tests: {str(e)}")
            raise

    def develop_features(self, specification):
        code, tokens_used = self.feature_developer.develop(specification)
        self.total_tokens_used += tokens_used
        return self.remove_markdown(code)

    def run_tests(self, tests, code):
        return self.test_runner.run_tests(tests, code)

    def improve_code(self, code, test_results):
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=min(2000, self.max_tokens) if self.max_tokens else 2000,
                messages=[
                    {"role": "user", "content": f"Improve this code to pass all tests. Provide only the improved code without any explanations or markdown formatting:\n{code}\nTest results: {test_results}"}
                ]
            )
            self.total_tokens_used += message.usage.output_tokens
            logging.info(f"Tokens used in improve_code: {message.usage.output_tokens}")
            return self.remove_markdown(message.content[0].text)
        except Exception as e:
            logging.error(f"Error in improve_code: {str(e)}")
            raise

    def remove_markdown(self, text):
        # Remove code block markers
        text = re.sub(r'```[\w]*\n|```', '', text)
        # Remove inline code markers
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Remove bold/italic markers
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        # Remove headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        return text.strip()

    def get_total_tokens_used(self):
        return self.total_tokens_used

# Remove the usage example from here as it's not needed in the class file