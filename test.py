from backend.analyzer import MockCommentAnalyzer
from backend.aggregator import Aggregator
from backend.instagram import Instagram
from backend.comments import parse_comments
from pprint import pp


comments = parse_comments(Instagram().get_comments("https://www.instagram.com/p/Ddk4uxwSNBd"))

analyzer = MockCommentAnalyzer()

analyses = analyzer.analyze_comments(comments)

aggregator = Aggregator()

report = aggregator.aggregate(analyses)

pp(report.model_dump())