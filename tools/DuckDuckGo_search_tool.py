import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import Field
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

# Set up your SERPER_API_KEY key in an .env file, eg:
# SERPER_API_KEY=<your api key>
load_dotenv()

search = DuckDuckGoSearchRun()

class DuckDuckGoSearchRunTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
    search: DuckDuckGoSearchRun = Field(default_factory=DuckDuckGoSearchRun)

    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"