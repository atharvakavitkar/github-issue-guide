import streamlit as st
import requests
import os
from dotenv import load_dotenv
from google.generativeai import configure
from git import Repo
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from data_utils import clone_repo, get_dir_struct_str, get_issue_details, create_documents
# Load environment variables
load_dotenv()

# Configure Google AI
configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Generative AI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)




def generate_guidance(clone_dir, repo_structure, issue_data):
    documents = create_documents(clone_dir)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Embed
    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)

    retriever = vectorstore.as_retriever()


    # 2. Incorporate the retriever into a question-answering chain.
    system_prompt = (
    """You are an expert open source software developer.
        provide step-by-step guidance for a beginner GitHub user on how to solve the given issue
        Use the following pieces of retrieved context to provide the guidance
        If you don't know the answer, say that you don't know.
        The repository structure is as follows: {repo_structure}
        Your response should be structured as follows:

        Issue Explanation:
        - Explain what the issue is about
        - Clarify any technical terms or concepts that a beginner might not understand
        - Explain why this issue is important to address

        Step-by-Step Guidance:
        Based on the retrieved context, repository structure and issue details, provide step-by-step guidance, specifying the exact lines of code to modify in order to resolve the issue.

        Provide clear, concise steps that a beginner can easily follow.
        \n\n
        {context}"""
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    #using only title and body of the issue
    issue_title_body = f"Title: {issue_data['title']} Description: {issue_data['body']}"

    guidance = rag_chain.invoke({"input": issue_title_body, "repo_structure": repo_structure})
    return guidance['answer']

st.title("GitHub Issue Guide")

issue_url = st.text_input("Enter GitHub issue URL")

if st.button("Get Guidance"):
    if issue_url:
        with st.spinner("Cloning repository..."):
            try:
                repo_url = issue_url.split("/issues")[0]
                repo, clone_dir = clone_repo(repo_url)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        with st.spinner("Extracting directory structure..."):            
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
                guidance = generate_guidance(clone_dir, repo_structure, issue_data)
                st.markdown(guidance)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a GitHub issue URL")