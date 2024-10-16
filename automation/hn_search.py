from datetime import datetime, timedelta
import requests


def search_hackernews(query: str = "orchestration", window_size_days: int = 7):
    url = "http://hn.algolia.com/api/v1/search"

    threshold = datetime.utcnow() - timedelta(days=window_size_days)

    params = {
        "query": query,
        "numericFilters": f"created_at_i>{threshold.timestamp()}",
    }

    response = requests.get(url, params).json()
    urls = [item["url"] for item in response["hits"] if "url" in item and item["url"]]
    print(f"Query returned {len(urls)} items.")
    print(urls)


if __name__ == "__main__":
    search_hackernews()
