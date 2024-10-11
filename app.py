import streamlit as st
import requests
import os
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
from git import Repo
# Load environment variables
load_dotenv()

# Configure Google AI
configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Generative AI model
model = GenerativeModel("gemini-1.5-flash")

def download_repo(repo_url):
    repo = None
    repo_dir = repo_url.split("/")[-1].split(".")[0]
    download_dir = os.path.join("temp",repo_dir)
    try:
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            print("Downloading Repo..")
            repo = Repo.clone_from(repo_url, download_dir)
            print("Download complete.")
        else:
            print("Repo already downloaded..")
            repo = Repo(download_dir)
    except Exception as e:
        print(e)
    return repo

def get_dir_struct_str(tree, indent_level=0):
    tree_str = ""
    indent = " " * (indent_level * 4)  # Indentation for readability

    for item in tree:
        if item.type == "tree":  # If it's a directory (tree)
            tree_str += f"{indent}{item.name} {{\n"  # Opening brace for directory
            tree_str += get_dir_struct_str(item, indent_level + 1)  # Recursively process subdirectories
            tree_str += f"{indent}}}\n"  # Closing brace for directory
        else:  # If it's a file (blob)
            tree_str += f"{indent}{item.name}\n"  # File name without braces

    return tree_str

def get_issue_details(issue_url):
    # Extract owner, repo, and issue number from the URL
    parts = issue_url.split('/')
    owner, repo = parts[-4], parts[-3]
    issue_number = parts[-1]
    
    # Fetch issue details from GitHub API
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}", headers=headers)
    print(response.json())
    return response.json()

def generate_guidance(issue_data):
    prompt = f"""As an expert GitHub guide, provide step-by-step guidance for a novice GitHub user on how to solve the following issue:

Title: {issue_data['title']}
Description: {issue_data['body']}

Your response should be structured as follows:

Issue Explanation:
  - Explain what the issue is about
  - Clarify any technical terms or concepts that a novice might not understand
  - Explain why this issue is important to address

Step-by-step Guidance:
   Include detailed information on:
    1. Setting up the development environment  
    2. Forking the repository  
    3. Creating a new branch  
    4. Making the necessary changes  
    5. Committing and pushing the changes  
    6. Creating a pull request

Provide clear, concise steps that a beginner can easily follow."""

    result = model.generate_content(prompt)
    return result.text

st.title("GitHub Issue Guide")

issue_url = st.text_input("Enter GitHub issue URL")

if st.button("Get Guidance"):
    if issue_url:
        with st.spinner("Downloading repository..."):
            try:
                repo_url = issue_url.split("/issues")[0]
                repo = download_repo(repo_url)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        with st.spinner("Creating directory structure..."):            
            try:
                # Get the root tree of the repo
                repo_tree = repo.tree()
        
                # Start the tree string with the repo root in curly braces
                repo_structure = f"repo {{\n{get_dir_struct_str(repo_tree, 1)}}}"
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        

        with st.spinner("Getting issue details..."):
            try:
                issue_data = get_issue_details(issue_url)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        with st.spinner("Generating guidance..."):
            try:
                guidance = generate_guidance(issue_data)
                st.markdown(guidance)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a GitHub issue URL")