from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json
from pydantic import BaseModel, field_validator, HttpUrl
from services import AnalysisService, ExtractorService, StreamResponseService
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import os

dotenv.load_dotenv()

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


ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "").split(',')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*']

)

analysis_service = AnalysisService()
extractor_service = ExtractorService()
stream_response_service = StreamResponseService()

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
            'error' : str(e)
        })

@app.post("/analyze/stream")
def analyze_stream(request : AnalyzeRequest):

    def event_generator():
        try:
            for event in stream_response_service.stream_analysis(
                url = str(request.url.url),
                model = str(request.model)
            ):
                yield f"data: {json.dumps(event)}\n\n"

        except Exception as e:
            error = {
                'type' : 'error',
                'data' : {
                    'error' : str(e)
                }
            }
            yield f"data: {json.dumps(error)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type= 'text/event-stream',
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
                


@app.post("/get_comments")
def get_comments(request : InstagramURL):
    try:
        return extractor_service.extract_comments(str(request.url))
    except Exception as e:
        raise HTTPException(400, detail= {'error' : str(e)})
    
