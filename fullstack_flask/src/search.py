from duckduckgo_search import DDGS
from itertools import islice

# List of preferred websites to search first
PREFERRED_SITES = [
    "www.apa.org",
    "www.nimh.nih.gov",
    "www.mbct.com",
    "www.verywellmind.com",
    "www.mhanational.org"
]

def search_news(keywords, num_results=10, preferred_sites=PREFERRED_SITES):
    """
    Search news using DuckDuckGo, prioritizing preferred sites first.
    If no results from preferred sites, it performs a general search.
    """
    result = []
    with DDGS() as ddgs:
        # First, search within preferred sites
        for site in preferred_sites:
            ddgs_news_gen = ddgs.news(
                f"site:{site} {keywords}",
                region="us-en",
                safesearch="Off",
                timelimit="m",
            )
            result.extend(islice(ddgs_news_gen, num_results // 2))  # Get half from preferred

        # If not enough results, perform a general search
        if len(result) < num_results:
            ddgs_news_gen = ddgs.news(
                keywords,
                region="us-en",
                safesearch="Off",
                timelimit="m",
            )
            result.extend(islice(ddgs_news_gen, num_results - len(result)))  # Get remaining

    return result

def search_text(keywords, num_results=10, preferred_sites=PREFERRED_SITES):
    """
    Search web using DuckDuckGo, prioritizing preferred sites first.
    If no results from preferred sites, it performs a general search.
    """
    result = []
    with DDGS() as ddgs:
        # First, search within preferred sites
        for site in preferred_sites:
            ddgs_text_gen = ddgs.text(
                f"site:{site} {keywords}",
                region='us-en',
                safesearch='Off',
                timelimit='y'
            )
            result.extend(islice(ddgs_text_gen, num_results // 2))  # Get half from preferred

        # If not enough results, perform a general search
        if len(result) < num_results:
            ddgs_text_gen = ddgs.text(
                keywords, 
                region='us-en', 
                safesearch='Off', 
                timelimit='y'
            )
            result.extend(islice(ddgs_text_gen, num_results - len(result)))  # Get remaining

    return result
