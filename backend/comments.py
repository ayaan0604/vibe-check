from dataclasses import dataclass
from typing import List

@dataclass
class Comment:
    id : str
    text : str
    created_at : int


def parse_comments(response) -> List[Comment]:
    comments = []

    for item in response['comments']:
        text = item.get('text', "").strip()

        if not text:
            continue

        comments.append(
            Comment(
                id = item['id'],
                text = text,
                created_at= item["created_at"]
            )
        )

    return comments

