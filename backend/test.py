from services import AnalysisService, StreamResponseService
from pprint import pp
from analyzer import LayaCommentAnalyzer
import time
import json

#pp(AnalysisService().analyze("https://www.instagram.com/p/Ddk4uxwSNBd", 'laya').model_dump())
from instagram import Instagram
from comments import parse_comments
from aggregator import Aggregator

start = time.perf_counter()

# pp(
    
#     Aggregator().aggregate(
#         LayaCommentAnalyzer().analyze_comments(
#             parse_comments(
#                 Instagram().get_comments("https://www.instagram.com/p/Ddk4uxwSNBd")
#             )
#         )
#     )
    
# )

# elapsed = time.perf_counter() - start
# print("elapsed: ", elapsed)

report = ((StreamResponseService().stream_analysis('https://www.instagram.com/p/Ddk4uxwSNBd', model='jev')))
for result in report:
    print(result)


