import os
from git import Repo
import glob
from langchain_core.documents import Document
from dotenv import load_dotenv

import requests
# Load environment variables
load_dotenv()


def clone_repo(repo_url):
    repo = None
    repo_dir = repo_url.split("/")[-1].split(".")[0]
    clone_dir = os.path.join("repositories",repo_dir)
    try:
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
            print("Downloading Repo..")
            repo = Repo.clone_from(repo_url, clone_dir)
            print("Download complete.")
        else:
            print("Repo already downloaded..")
            repo = Repo(clone_dir)
    except Exception as e:
        print(e)
    return repo, clone_dir


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


def extract_files(clone_dir):
    """Extract files from the cloned repository."""
    file_paths = []
    # Find all relevant files in the cloned repository
    for ext in ['*.py', '*.js', '*.java', '*.md', '*.txt', '*.c', '*.cpp', '*.html']:
        file_paths.extend(glob.glob(os.path.join('**', ext), recursive=True))
    return file_paths

def create_chunks(file_path, chunk_size=256, chunk_overlap=64):
    """Split content into manageable chunks with optional overlap, preserving newlines."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content by lines and keep newline characters
    lines = content.splitlines(keepends=True)
    chunks = []
    current_chunk = []

    for line in lines:
        # Check if adding the line will exceed the chunk_size
        if len(''.join(current_chunk)) + len(line) <= chunk_size:
            current_chunk.append(line)
        else:
            # Finalize the current chunk
            current_doc = Document(page_content=''.join(current_chunk), metadata={"origin": file_path})
            chunks.append(current_doc)
            
            # Handle overlap: Take the last `chunk_overlap` characters from the last chunk
            overlap_content = ''.join(current_chunk)[-chunk_overlap:] if current_chunk else ''
            
            # Start the new chunk with overlap, preserving the overlap characters
            current_chunk = [overlap_content + line] if overlap_content else [line]

    # Add any remaining content as the final chunk
    if current_chunk:
        current_doc = Document(page_content=''.join(current_chunk), metadata={"origin": file_path})
        chunks.append(current_doc)

    return chunks

def create_documents(repo_dir):
    """Main function to create a knowledge base from a GitHub repo."""
    
    # Step 2: Extract relevant files
    file_paths = extract_files(repo_dir)
    # Step 3: Create chunks
    documents = []
    for file_path in file_paths:
        chunks = create_chunks(file_path, chunk_size=256, chunk_overlap=64)
        if chunks: documents.extend(chunks)

    print(f'Documents created with {len(file_paths)} files.')
    return documents
    
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


