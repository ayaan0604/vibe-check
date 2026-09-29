from instagram import Instagram
from comments import parse_comments
from analyzer import JevCommentAnalyzer, MockCommentAnalyzer, LayaCommentAnalyzer
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
        self.analyzers_map = {
            'jev' : JevCommentAnalyzer,
            'laya' : LayaCommentAnalyzer()
        }
        self.mock_analyzer = MockCommentAnalyzer()
        self.mock_active = False
        self.aggregator = Aggregator()
        self.cache = AnalysisCache()

    def get_analysed_comments(self, comments, model):
        if model not in self.analyzers_map.keys():
            raise Exception(f"Please choose a model opition from : {self.analyzers_map.keys()}")
        
        if model == 'jev':
            return self.jev_analysis(comments)
        if model == "laya":
            return self.laya_analysis(comments)

    def jev_analysis(self, comments) -> AnalysisReport:
        with self.analyzers_map['jev'] as analyzer:
           return analyzer.analyze_comments(comments)

    def laya_analysis(self, comments):
        return self.analyzers_map['laya'].analyze_comments(comments)
    
    def analyze(self, url:str, model: str):

        key = f'{self.instagram.get_media_code(url)}_{model}'

        comments = parse_comments(
            self.instagram.get_comments(
                url=url,
                sort_order='popular'
            )
        )

        cached = self.cache.get(key)
        if cached is not None:
            report =  AnalysisReport.model_validate(cached)
            report.comments = [comment.__dict__ for comment in comments]
            return report

        if self.mock_active:
            analysed = self.mock_analyzer.analyze_comments(comments)

        
        else:
            analysed = self.get_analysed_comments(comments, model)

        report = self.aggregator.aggregate(analysed)

        self.cache.set(key = key, data = report.model_dump())

        report.comments = report.comments = [comment.__dict__ for comment in comments]

        return report


        
class ExtractorService():
    def __init__(self):
        self.instagram = Instagram()
        self.comment_parser = parse_comments

    def extract_comments(self, url: str):
        comments = self.comment_parser(
            self.instagram.get_comments(url)
        )
        return {
            'comments' :
            [comment.__dict__ for comment in comments]
            }
    