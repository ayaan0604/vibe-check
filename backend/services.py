from instagram import Instagram
from comments import parse_comments
from analyzer import JevCommentAnalyzer, MockCommentAnalyzer
from aggregator import Aggregator, AnalysisReport
import time
from pathlib import Path
import json


_24_hours_in_second = 86400

class AnalysisCache:
    def __init__(self, cache_dir : str = "cache/analysis", ttl: int = _24_hours_in_second):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.ttl = ttl

    def _get_path(self, key:str)->Path:
        return self.cache_dir / f'{key}.json'

    def get(self, key):
        path = self._get_path(key)

        if not path.exists():
            return None

        with open(path, "r") as file:
            cached = json.load(file)

        age = time.time() - cached['created_at']

        if age >= self.ttl:
            path.unlink()
            return None

        return cached['data']

    def set(self, key: str, data):
        path = self._get_path(key)

        cached = {
            'created_at' : time.time(),
            "data" : data
        }

        with open(path, "w") as file:
            json.dump(cached, file, indent=2)




class AnalysisService:
    def __init__(self):
        self.instagram = Instagram()
        self.comments_analyzer = JevCommentAnalyzer
        self.mock_analyzer = MockCommentAnalyzer()
        self.mock_active = True
        self.aggregator = Aggregator()
        self.cache = AnalysisCache()

    def analyze(self, url:str):

        key = self.instagram.get_media_code(url)

        cached = self.cache.get(key)
        if cached is not None:
            return AnalysisReport.model_validate(cached)

        comments = parse_comments(
            self.instagram.get_comments(
                url=url,
                sort_order='popular'
            )
        )

        if self.mock_active:
            analysed = self.mock_analyzer.analyze_comments(comments)

        
        else:
            with self.comments_analyzer() as analyzer:
                analysed = analyzer.analyze_comments(comments)

        report = self.aggregator.aggregate(analysed)

        self.cache.set(key = key, data = report.model_dump())

        return report


        

