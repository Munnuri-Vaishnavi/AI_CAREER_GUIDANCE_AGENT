from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from config import TAVILY_API_KEY
import os

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

search_tool = TavilySearchResults(max_results=3)

@tool
def search_exam_notifications(query: str) -> str:
    """Search for latest exam notifications and dates in India."""
    return str(search_tool.invoke(query + " official notification 2025"))

@tool
def search_college_cutoffs(query: str) -> str:
    """Search for college cutoffs and admission details in AP and Telangana."""
    return str(search_tool.invoke(query + " cutoff 2024 2025 AP Telangana"))

@tool
def search_scholarship_details(query: str) -> str:
    """Search for scholarship eligibility and application details."""
    return str(search_tool.invoke(query + " scholarship eligibility apply 2025"))

@tool
def search_govt_job_notifications(query: str) -> str:
    """Search for government job notifications from APPSC TSPSC SSC Railways Police."""
    return str(search_tool.invoke(query + " recruitment notification 2025"))

@tool
def search_career_salary_trends(query: str) -> str:
    """Search for salary trends and job demand for careers in India."""
    return str(search_tool.invoke(query + " salary India 2025 job demand"))

def get_search_tools():
    return [
        search_exam_notifications,
        search_college_cutoffs,
        search_scholarship_details,
        search_govt_job_notifications,
        search_career_salary_trends,
    ]