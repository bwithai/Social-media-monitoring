from datetime import datetime

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from X.do_engage_on_tweet import do_impression_on
from schemas import CrawlerSchema
from X.get_tweets import get_tweets
from database.mongo_client import x_collection

x_router = APIRouter(prefix="/v1-X", tags=["X (Twitter)"])


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError


@x_router.post('/fetch-tweets')
async def fetch_tweets(request: CrawlerSchema):
    try:
        tweet_data = get_tweets(username=request.username, days=request.days)
        if tweet_data:
            try:
                x_collection.insert_many(tweet_data)
                return JSONResponse(content={"message": f"{request.days} days post(s) have been saved to Database"},
                                    status_code=200)
            except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
                return JSONResponse(
                    content={"Error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "Details": str(db_error)}, status_code=500)
        else:
            return JSONResponse(content={"Message": "Scraping Failed"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)


@x_router.post('/engagement-on-tweets')
async def fetch_tweets(tweet_url: str, send_message: str):
    try:
        response = do_impression_on(tweet_url=tweet_url, reply_message=send_message)
        if response:
            try:
                return JSONResponse(content={"message": "" + response},
                                    status_code=200)
            except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
                return JSONResponse(
                    content={"Error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "Details": str(db_error)}, status_code=500)
        else:
            return JSONResponse(content={"Message": f"Engagement Failed on tweet: {tweet_url}"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)
