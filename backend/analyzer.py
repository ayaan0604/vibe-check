from typing import Literal
from pydantic import BaseModel
from typesafe_sdk import Choice, Score, Noul, TypeSafeClient
from .comments import Comment
import random
from typing import List
class CommentAnalysis(BaseModel):

    comment_id : str

    intent : Literal[
        "HYPE",
        "ROAST",
        "WANDER",
        "JOKE",
        "REACTION",
        "SUGGESTION",
        "STORY",
        "OTHER"
    ]

    reaction : Literal[
        "LOL",
        "HAPPY",
        "DOWNFALL",
        "FLABBERGASTED",
        "ANGRY",
        "CONFUSED",
        "NEUTRAL",
        "COOKED"
    ]

    # language_style: Literal[
    #     "GEN_ALPHA",
    #     "GEN_Z",
    #     "MILLENNIAL",
    #     "GEN_X_OR_BOOMER",
    #     "NEUTRAL"
    # ]

    sarcastic: bool





class CommentAnalyzer:
    def analyze(self, comment: Comment) -> CommentAnalysis:
        raise NotImplementedError

class MockCommentAnalyzer(CommentAnalyzer):
    intent_options = [
        "HYPE",
        "ROAST",
        "WANDER",
        "JOKE",
        "REACTION",
        "SUGGESTION",
        "STORY",
        "OTHER"
    ]
    
    reaction_options = [
        "LOL",
        "HAPPY",
        "DOWNFALL",
        "FLABBERGASTED",
        "ANGRY",
        "CONFUSED",
        "NEUTRAL",
        "COOKED"
    ]

    def analyze(self, comment: Comment) -> CommentAnalysis:
        return CommentAnalysis(
            comment_id = comment.id,
            intent= random.choice(self.intent_options),
            reaction= random.choice(self.reaction_options),
            sarcastic= random.choice([True, False])
        )

    def analyze_comments(self, comments: List[Comment])-> List[CommentAnalysis]:
        analyzed = []
        for comment in comments:
            analyzed.append(
                self.analyze(comment)
            )
        return analyzed

class JevCommentAnalyzer(CommentAnalyzer):
    def __init__(self):
        self.client = None

        self.questions = {
            "intent": Choice(
                instructions="What is the primary intent of this Instagram comment?",
                criteria={
                    "hype": "The commenter is expressing approval, admiration, or positive appreciation.",
                    "roast": "The commenter is expressing disapproval or a negative opinion.",
                    "wander": "The commenter is primarily asking for information.",
                    "joke": "The comment is primarily intended as humor.",
                    "reaction": "The comment mainly expresses an immediate emotional reaction.",
                    "suggestion": "The commenter is recommending or requesting a change or action.",
                    "story": "The commenter is sharing a personal experience or story.",
                    "other": "The comment does not clearly fit the other categories.",
                },
            ),
            "reaction": Choice(
                instructions="What is the primary emotional reaction expressed by this comment?",
                criteria={
                    "lol": "The comment expresses amusement or humor.",
                    "happy": "The comment expresses happiness or excitement.",
                    "downfall": "The comment expresses sadness.",
                    "flabbergasted": "The comment expresses surprise or disbelief.",
                    "angry": "The comment expresses anger or frustration.",
                    "confused": "The comment expresses confusion.",
                    "neutral": "No clear emotional reaction is expressed.",
                    "cooked" : "Realisation of being in a bad or dangerous state"
                },
            ),
            "sarcastic": Noul(
                instructions="Is the comment sarcastic?",
                criteria={
                    "true": "The comment communicates something ironically or mockingly rather than literally.",
                    "false": "The comment is sincere or does not contain clear sarcasm.",
                },
            ),
        }

    def __enter__(self):
        self.client = TypeSafeClient
        self.client.__enter__()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.__exit__(exc_type, exc_value, traceback)

    def analyze(self, comment):
        if self.client is None:
            raise RuntimeError("JevCommentAnalyzer must be used within a with block")

        response = self.client.system_one(
            state = {'commment' : comment.text},
            questions= self.questions
        )

        return CommentAnalysis(
            comment_id= comment.id,
            intent = response.answers["intent"].choice.upper(),
            reaction = response.answers["reaction"].choice.upper(),
            sarcastic = response.answers["sarcastic"].choice.upper(),
        )

    def analyze_comments(
            self,
            comments : List[Comment]
    ) -> List[CommentAnalysis]:

        return [
            self.analyze(comment) for comment in comments
        ]
    