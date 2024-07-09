from fastapi import APIRouter
from starlette.responses import JSONResponse
from schemas import X_Schema
from X.get_tweets import get_tweets

x_router = APIRouter(prefix="/v1-X", tags=["X (Twitter)"])


@x_router.post('/fetch-tweets')
async def fetch_tweets(request: X_Schema):
    try:
        tweet_date = get_tweets(username=request.username, days=request.days)
        return JSONResponse(content={"tweets": tweet_date}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
