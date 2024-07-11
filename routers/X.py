import json
from datetime import datetime

from fastapi import APIRouter
from starlette.responses import JSONResponse
from schemas import X_Schema
from X.get_tweets import get_tweets
from database.mongo_client import x_collection

x_router = APIRouter(prefix="/v1-X", tags=["X (Twitter)"])


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError


@x_router.post('/fetch-tweets')
async def fetch_tweets(request: X_Schema):
    try:
        tweet_data = get_tweets(username=request.username, days=request.days)
        if tweet_data:
            if tweet_data:
                x_collection.insert_many(tweet_data)
                return JSONResponse(content={"message": f"{request.days} days of tweet has been saved to Database"},
                                    status_code=200)
                # return JSONResponse(content={"tweets": json.dumps(tweet_data, default=json_default)}, status_code=200)
            else:
                return JSONResponse(content={"Message": "Scraping Failed"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)
