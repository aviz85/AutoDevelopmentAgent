import anthropic

class FeatureDeveloper:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def develop(self, specification):
        prompt = f"Develop Python code for the following specification:\n\n{specification}\n\nProvide only the code, no explanations."
        response = self.client.completions.create(
            model="claude-3-sonnet-20240229",
            max_tokens_to_sample=2000,
            prompt=prompt
        )
        return response.completion