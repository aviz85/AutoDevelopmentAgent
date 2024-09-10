import streamlit as st
import logging
from agent import AutoDevelopmentAgent
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

def main():
    st.title("AutoDevelopmentAgent")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("ANTHROPIC_API_KEY is not set in the .env file")
        return

    agent = AutoDevelopmentAgent(api_key)

    idea = st.text_input("Enter your idea for a software application:")
    
    if st.button("Generate Code"):
        if idea:
            with st.spinner("Generating code... This may take a few minutes."):
                try:
                    logging.info(f"Processing idea: {idea}")
                    final_code = agent.process_user_idea(idea)
                    
                    st.success("Code generation complete!")
                    st.code(final_code, language="python")

                    # Save the final code to a file
                    with open("final_code.py", "w") as f:
                        f.write(final_code)
                    st.info("Final code has been saved to 'final_code.py'")
                    
                    logging.info("Code generation successful")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    logging.error(f"Error during code generation: {str(e)}")
        else:
            st.warning("Please enter an idea before generating code.")

if __name__ == "__main__":
    main()