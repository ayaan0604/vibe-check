import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
X_RAPIDAPI_KEY = os.environ.get('X_RAPIDAPI_KEY')
X_RAPIDAPI_HOST = "instagram-scraper-stable-api.p.rapidapi.com"


class Instagram:
    def __init__(self, rapid_api_key = X_RAPIDAPI_KEY, rapid_api_host = X_RAPIDAPI_HOST):

        self.rapid_api_key = rapid_api_key
        self.rapid_api_host = rapid_api_host

        self.cache_dir = Path("cache/instagram")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_media_code(self, url : str) -> str:
        url_parts = url.split("?")[0].strip('/').split("/")
        return url_parts[-1]

    def get_cached_comments(self, media_code: str):
        cache_file = self.cache_dir / f"{media_code}.json"

        if not cache_file.exists():
            return None

        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_cached_comments(self, media_code: str, data):
        cache_file = self.cache_dir / f"{media_code}.json"

        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_comments(self, url: str, sort_order : str = "recent"):
        '''- sort order can be 'recent' or 'popular' -'''
    
        media_code = self.get_media_code(url)
        print(media_code)

        cached = self.get_cached_comments(media_code)


        if cached is not None:
            print("returning cached data")
            return cached

        print("calling api")
        
        api_url = "https://instagram-scraper-stable-api.p.rapidapi.com/get_post_comments.php"

        querystring = {
            "sort_order" : sort_order,
            "media_code" : media_code
        }

        headers = {
            "x-rapidapi-key": self.rapid_api_key,
            "x-rapidapi-host": self.rapid_api_host
        }

        response = requests.get(api_url, headers=headers, params=querystring)

        response.raise_for_status()

        data = response.json()
        
        self.save_cached_comments(data = data, media_code = media_code)

        return data

      
if __name__ == "__main__":
    
    i = Instagram()
    comments = i.get_comments("https://www.instagram.com/p/Ddk4uxwSNBd")

    print(len(comments['comments']))
