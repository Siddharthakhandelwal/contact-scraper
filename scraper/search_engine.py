# scraper/search_engine.py
from googlesearch import search
from config import SEARCH_KEYWORDS
#
def get_search_results(query, num_results=100):
    try:
        return list(search(query, num_results=num_results))
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def run_queries():
    all_links = []
    for query in SEARCH_KEYWORDS:
        print(f"[🔍] Searching for: {query}")
        links = get_search_results(query)
        all_links.extend(links)
    return list(set(all_links))  # remove duplicates
