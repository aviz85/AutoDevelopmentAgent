# AutoDevelopmentAgent

AutoDevelopmentAgent is a Python-based tool that uses the Anthropic API to autonomously develop software based on user ideas. It creates specifications, plans tests, develops features, runs tests, and improves code iteratively.

## Prerequisites

- Python 3.7+
- Anthropic API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/aviz85/AutoDevelopmentAgent.git
   cd AutoDevelopmentAgent
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your Anthropic API key:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file and replace `your_api_key_here` with your actual Anthropic API key.

## Usage

### Web Interface

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually `http://localhost:8501`).

3. Enter your idea for a software application in the text input field and click "Generate Code".

4. The generated code will be displayed in the browser and saved to `final_code.py`.

### Command Line Interface

1. Run the main script:
   ```
   python main.py
   ```

2. When prompted, enter your idea for a software application.

3. The agent will process your idea and generate code. This may take a few minutes depending on the complexity of your idea.

4. Once complete, the final code will be displayed in the console and saved to a file named `final_code.py` in the current directory.

## File Structure

- `app.py`: Streamlit web application for the AutoDevelopmentAgent.
- `main.py`: Command-line interface for the AutoDevelopmentAgent.
- `agent.py`: Contains the `AutoDevelopmentAgent` class, which orchestrates the development process.
- `feature_developer.py`: Handles the feature development based on specifications.
- `test_runner.py`: Manages test creation and execution.
- `.env`: Contains environment variables (not tracked by git).
- `.gitignore`: Specifies files that Git should ignore.
- `requirements.txt`: Lists all Python dependencies for the project.

## Customization

You can modify the `max_iterations` variable in `agent.py` to change the maximum number of improvement iterations the agent will perform.

## Limitations

- The quality of the generated code depends on the capabilities of the Anthropic API.
- Complex ideas may require manual intervention or refinement.
- The agent may not always produce perfect or complete code, especially for large or complex projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
