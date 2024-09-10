import anthropic

class FeatureDeveloper:
    def __init__(self, api_key):
        self.client = anthropic.Client(api_key)

    def develop(self, specification):
        prompt = f"Develop Python code for the following specification:\n\n{specification}\n\nProvide only the code, no explanations."
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content