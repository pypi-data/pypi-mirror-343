import os
import subprocess
from typing import Literal

import requests
from bs4 import BeautifulSoup

from aicli.agentlib import get_general_agent


def run_command(command: str):
    """
    Execute the given command line instruction.

    Args:
        command (str): The command line instruction to be executed.

    Returns:
        str: The standard output result of the command execution.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def install_package(package_name: str):
    """
    Install the specified Python package using pip.

    Args:
        package_name (str): The name of the package to be installed.

    Returns:
        str: The standard output result of the installation process.
    """
    command = f'pip install {package_name}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout


def web_search(
    query: str,
    search_depth: Literal["basic", "advanced"] = "basic",
    topic: Literal["general", "news"] = "general",
    days: int = 3,
    max_results: int = 5,
    include_answer: bool = False,
    include_raw_content: bool = False,
    include_images: bool = False,
) -> dict:
    """
    Perform a web search using the Tavily API.

    This function uses the TavilyClient to search the web based on the provided parameters.
    It returns the search results as obtained from the API.

    Args:
        query (str): The search query to be used for the web search.
        topic (str, optional): The topic of the search. Defaults to "general", can also be "news".
        search_depth (str, optional): The depth of the search. Can be "basic" or "advanced". Defaults to "basic".
        max_results (int, optional): The maximum number of search results to return. Defaults to 5.
        days (int): the latest days to search.
        include_answer (bool): Include answer from llm.
        include_images (bool): Include image urls in search results.
        include_raw_content (bool): Include raw content in search results.

    Returns:
        dict: The response from the Tavily API containing the search results.

        {
            "query": str,
            "follow_up_questions": null,
            "answer": null,
            "images": [],
            "results": [
                {
                "url": str,
                "title": str,
                "content": str,
                "score": float,
                "raw_content": null
                },
                ...
            ],
            "response_time": float
        }

    Raises:
        Exception: If there's an error in the API call or if the API key is not set correctly.
    """
    from tavily import TavilyClient
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(
        query=query,
        topic=topic,
        search_depth=search_depth,
        max_results=max_results,
        days=days,
        include_answer=include_answer,
        include_images=include_images,
        include_raw_content=include_raw_content,
    )
    return response


def translate(content: str, target_lang: str):
    """Translate content to target language."""
    agent = get_general_agent(model=os.getenv("MODEL"))
    return agent.run(f'translate <CONTENT>{content}</CONTENT> to {target_lang}')


def read_link(url: str) -> str:
    """Read url content as str."""
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        return soup.text
    return "read link failed."