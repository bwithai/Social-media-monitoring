from datetime import datetime

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from social_media.do_engage_on_tweet import do_impression_on
from database.queries import add_crawler_data, get_x_by_id
from schemas import CrawlerSchema
from social_media.X import get_tweets
from utils import serialize_object_id, serialize_datetime

router = APIRouter(prefix="/x", tags=["X (Twitter)"])


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError


@router.post('/fetch-tweets')
async def fetch_tweets(request: CrawlerSchema):
    try:
        tweet_data = get_tweets(username=request.username, days=request.days)
        if tweet_data:
            result = add_crawler_data(request, tweet_data, 'X')
            if isinstance(result, Exception):
                return JSONResponse(
                    content={"Error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "Details": str(result)}, status_code=500)
            else:
                return JSONResponse(content={"message": result},
                                    status_code=200)
        else:
            return JSONResponse(content={"Message": "Scraping Failed"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)


@router.post('/engagement-on-tweets')
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


@router.get('/get-by-id')
async def get_user(tweets_id: str):
    tweets = get_x_by_id(tweets_id)
    if tweets:
        tweets = serialize_datetime(tweets)
        tweets = serialize_object_id(tweets)
        return JSONResponse(
            content=tweets,
            status_code=200
        )
    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )
