from fastapi import FastAPI
from pydantic import BaseModel, field_validator, HttpUrl
from services import AnalysisService


class AnalyzeRequest(BaseModel):
    url : HttpUrl

    @field_validator('url')
    @classmethod
    def validate_instagram_url(cls, value):
        if value.host not in {'instagram.com', 'www.instagram.com'}:
            raise ValueError("URL must be an Instagram URL")

        
        path = value.path.strip("/").split("/")

        if len(path) < 2 or path[0] not in {"p", "reel", "reels"}:
            raise ValueError(
                "URL must be an Instagram post, reel, or video URL"
            )

        return value




app = FastAPI()

service = AnalysisService()

@app.get('/health')
def health():
    return {
        "status" : "ok"
    }

@app.post('/analyze')
def analyze(request: AnalyzeRequest):
    return service.analyze(str(request.url))