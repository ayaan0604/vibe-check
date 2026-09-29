from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator, HttpUrl
from services import AnalysisService, ExtractorService


class InstagramURL(BaseModel):
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

class AnalyzeRequest(BaseModel):
    url : InstagramURL
    model : str




app = FastAPI()

analysis_service = AnalysisService()
extractor_service = ExtractorService()

@app.get('/health')
def health():
    return {
        "status" : "ok"
    }

@app.post('/analyze')
def analyze(request: AnalyzeRequest):
    try:
        return analysis_service.analyze(str(request.url.url), str(request.model))
    except Exception as e:
        raise HTTPException(status_code=400, detail={
            'error' : e
        })

@app.post("/get_comments")
def get_comments(request : InstagramURL):
    try:
        return extractor_service.extract_comments(str(request.url))
    except Exception as e:
        raise HTTPException(400, detail= {'error' : e})
    
