from datetime import datetime

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from social_media.facebook import get_fb_posts
from database.queries import add_crawler_data, get_fb_posts_by_id
from schemas import CrawlerSchema
from database.mongo_client import fb_collection
from utils import serialize_object_id

route = APIRouter(prefix="/fb", tags=["Facebook"])


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError


@route.post('/fetch-fb-posts')
async def fetch_fb_post(request: CrawlerSchema):
    try:
        post_data = get_fb_posts(username=request.username, days=request.days)
        if post_data:
            result = add_crawler_data(request, post_data, 'facebook')
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


@route.get('/get-by-id')
async def get_user(posts_id: str):
    fb_posts = get_fb_posts_by_id(posts_id)
    if fb_posts:
        return JSONResponse(
            content=serialize_object_id(fb_posts),
            status_code=200
        )
    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )
