import anthropic
import logging
import re
from dotenv import load_dotenv

class FeatureDeveloper:
    def __init__(self, max_tokens=None):
        load_dotenv()
        self.client = anthropic.Anthropic()
        logging.info("Anthropic client initialized successfully in FeatureDeveloper")
        self.max_tokens = max_tokens

    def develop(self, specification):
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=min(2000, self.max_tokens) if self.max_tokens else 2000,
                messages=[
                    {"role": "user", "content": f"Develop Python code for the following specification:\n\n{specification}\n\nProvide only the code, no explanations or markdown formatting."}
                ]
            )
            tokens_used = message.usage.output_tokens
            logging.info(f"Tokens used in FeatureDeveloper.develop: {tokens_used}")
            return self.remove_markdown(message.content[0].text), tokens_used
        except Exception as e:
            logging.error(f"Error in FeatureDeveloper.develop: {str(e)}")
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