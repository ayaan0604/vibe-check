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
        self.mock_active = True
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
        print("key:",key)
        cached = self.cache.get(key)
        if cached is not None:
            report =  AnalysisReport.model_validate(cached)
            return report

        comments = parse_comments(
            self.instagram.get_comments(
                url=url,
                sort_order='popular'
            )
        )

        

        if self.mock_active:
            analysed = self.mock_analyzer.analyze_comments(comments)

        
        else:
            analysed = self.get_analysed_comments(comments, model)

        report = self.aggregator.aggregate(analysed)

        self.cache.set(key = key, data = report.model_dump())

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

class StreamResponseService:
    def __init__(self):
        self.instagram = Instagram()
        self.comment_parser = parse_comments

        self.mock_analyzer = MockCommentAnalyzer()
        self.mock_active = False

        self.analyzer_map = {
            'jev' : JevCommentAnalyzer,
            'laya' : LayaCommentAnalyzer()
        }

        self.aggregator = Aggregator()
        self.cache = AnalysisCache()

    def stream_analysis(self, url:str, model: str):

        if model not in self.analyzer_map.keys():
            raise ValueError(f"Unknown Model : {model}. Choose from : {self.analyzer_map.keys()}")

        #laya currently not available on production, only for testing
        if model == "laya":
            yield {
                "type" : "error",
                "data" : {
                    'error' : 'Laya is not working currently, please choose any other model'
                }
            }
            
            return
    

        key = f"{self.instagram.get_media_code(url)}_{model}" 

        cached = self.cache.get(key)

        if cached is not None:
            yield {
                'type' : "cached",
                'data' : cached
            }
            return

    
        comments = self.comment_parser(
            self.instagram.get_comments(url)
        )
        if len(comments) == 0:
            yield {
                    "type" : "error",
                    "data" : {
                        'error' : f"Couldn't Retrieve Comments from {url}, try checking the url"
                    }
                }
            return

        yield {
            "type" : "starting",
            "data" : {
                "comments_fetched" : len(comments),
                "model" : model
            }
        }

        analysed = []

        analyzer = self.mock_analyzer if self.mock_active else self.analyzer_map[model]

        #jev needs a context manager
        if model == 'jev' and not self.mock_active:
           

            with analyzer() as jev_analyser:
                for idx, comment in enumerate(comments):
                    result = jev_analyser.analyze(comment)
                    analysed.append(result)

                    yield {
                        "type" : "comment",
                        "data" : {
                            'index' : idx,
                            'total' : len(comments),
                            'data' : result.model_dump()
                        }
                    }


        #for models other than jev
        else:
            for idx, comment in enumerate(comments):

                result = analyzer.analyze(comment)
                analysed.append(result)

                yield {
                    "type" : "comment",
                    "data" : {
                        'index' : idx,
                        'total' : len(comments),
                        'data' : result.model_dump()
                    }
                }

        #all comments are analysed
        report = self.aggregator.aggregate(analysed)

        self.cache.set(key = key, data = report.model_dump())

        yield {
            'type' : 'final_report',
            'data' : report.model_dump()
        }