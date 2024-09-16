# GitHub Issue Guide

## Description

GitHub Issue Guide is a Streamlit-based web application that provides step-by-step guidance for new and eager to contribute GitHub users on how to solve specific GitHub issues. By leveraging the power of Google's Generative AI, this tool offers detailed explanations and instructions tailored to each issue.

## Features

- Parse GitHub issue URLs
- Fetch issue details using GitHub API
- Generate comprehensive guidance using Google's Generative AI
- User-friendly interface built with Streamlit

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/github-issue-guide.git
   cd github-issue-guide
   ```

2. Create a virtual environment:
   ```
   python -m venv gig
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     gig\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source gig/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   GITHUB_TOKEN=your_github_token_here
   ```

## Usage

1. Ensure your virtual environment is activated.

2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

4. Enter a GitHub issue URL in the input field and click "Get Guidance".

5. The app will generate and display step-by-step guidance for solving the issue.

## Dependencies

- streamlit
- requests
- python-dotenv
- google-generativeai

For a complete list of dependencies, see `requirements.txt`.

## Contributing

Contributions to the GitHub Issue Guide project are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Generative AI for providing the AI model
- GitHub for their API
- Streamlit for the web app framework
