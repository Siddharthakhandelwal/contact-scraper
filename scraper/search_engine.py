# scraper/search_engine.py
from googlesearch import search
from config import get_keywords_for_domain, DEFAULT_KEYWORDS
import random
import time

def get_search_results(queries, num_results=100):
    """Search for multiple queries and return combined results"""
    all_results = []
    for query in queries:
        try:
            results = list(search(query, num_results=num_results))
            all_results.extend(results)
            # Random delay between searches to avoid rate limiting
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"Error searching for '{query}': {e}")
    return list(set(all_results))  # Remove duplicates

def run_queries(domain=None):
    """Run search queries for a specific domain"""
    keywords = get_keywords_for_domain(domain) if domain else DEFAULT_KEYWORDS
    print(f"[🔍] Searching with keywords: {', '.join(keywords)}")
    return get_search_results(keywords)
