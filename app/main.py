import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


class Agent:
    def __init__(self, llm):
        self.llm = llm

    def extract_jobs(self, data):
        # Logic for extracting jobs from the data
        return self.llm.extract_jobs(data)

    def write_mail(self, job, links):
        # Logic for writing the email
        return self.llm.write_mail(job, links)


def create_streamlit_app(llm, portfolio, clean_text, agent):
    st.title("📧 Job Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Load data from the URL
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load the portfolio
            portfolio.load_portfolio()

            # Use the agent to extract jobs and generate emails
            jobs = agent.extract_jobs(data)  # Use the agent for job extraction
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = agent.write_mail(job, links)  # Use the agent for writing the email
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    llm = chain  # Assuming your Chain instance acts as the LLM
    agent = Agent(llm)  # Create an instance of the Agent class
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(llm, portfolio, clean_text, agent)  # Pass the agent to the app
