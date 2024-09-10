import streamlit as st
import logging
from agent import AutoDevelopmentAgent
from dotenv import load_dotenv
import os
import time
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

class StreamlitLogger:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        self.log = ""

    def info(self, message):
        self.log += f"INFO: {message}\n"
        self.placeholder.text(self.log)

    def error(self, message):
        self.log += f"ERROR: {message}\n"
        self.placeholder.text(self.log)

def main():
    st.title("AutoDevelopmentAgent")

    # Add a token limit input
    token_limit = st.number_input("Set token limit (leave 0 for no limit)", min_value=0, value=0, step=1000)
    max_tokens = token_limit if token_limit > 0 else None

    # Initialize the agent with the token limit
    agent = AutoDevelopmentAgent(max_tokens)

    idea = st.text_input("Enter your idea for a software application:")
    
    if st.button("Generate Code"):
        if idea:
            # Create placeholders for logs and code
            log_placeholder = st.empty()
            code_placeholder = st.empty()

            # Create a custom logger that updates the Streamlit UI
            streamlit_logger = StreamlitLogger(log_placeholder)

            try:
                streamlit_logger.info(f"Processing idea: {idea}")
                
                # Step 1: Create specification
                streamlit_logger.info("Creating specification...")
                specification = agent.create_specification(idea)
                code_placeholder.code(specification, language="text")
                streamlit_logger.info(f"Tokens used: {agent.get_total_tokens_used()}")
                time.sleep(1)  # Add a small delay for visual effect

                # Step 2: Plan tests
                streamlit_logger.info("Planning tests...")
                tests = agent.plan_tests(specification)
                if tests:
                    code_placeholder.code(json.dumps(tests, indent=2), language="json")
                else:
                    streamlit_logger.warning("No tests were generated. Continuing without tests.")
                streamlit_logger.info(f"Tokens used: {agent.get_total_tokens_used()}")
                time.sleep(1)

                # Step 3: Develop features
                streamlit_logger.info("Developing features...")
                code = agent.develop_features(specification)
                code_placeholder.code(code, language="python")
                streamlit_logger.info(f"Tokens used: {agent.get_total_tokens_used()}")
                time.sleep(1)

                # Step 4: Run tests and improve code
                iteration = 0
                max_iterations = 5
                while iteration < max_iterations:
                    streamlit_logger.info(f"Running tests - Iteration {iteration + 1}")
                    test_results = agent.run_tests(tests, code)
                    
                    if all(test_results):
                        streamlit_logger.info("All tests passed!")
                        break
                    
                    streamlit_logger.info(f"Improving code - Iteration {iteration + 1}")
                    code = agent.improve_code(code, test_results)
                    code_placeholder.code(code, language="python")
                    streamlit_logger.info(f"Tokens used: {agent.get_total_tokens_used()}")
                    time.sleep(1)
                    
                    iteration += 1

                st.success("Code generation complete!")
                
                # Save the final code to a file
                with open("final_code.py", "w") as f:
                    f.write(code)
                st.info("Final code has been saved to 'final_code.py'")
                
                streamlit_logger.info("Code generation successful")
                st.success(f"Total tokens used: {agent.get_total_tokens_used()}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                streamlit_logger.error(f"Error during code generation: {str(e)}")
        else:
            st.warning("Please enter an idea before generating code.")

if __name__ == "__main__":
    main()