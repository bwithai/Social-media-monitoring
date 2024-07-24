from datetime import datetime

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from FB.get_posts import get_fb_posts
from schemas import CrawlerSchema
from database.mongo_client import fb_collection

fb_router = APIRouter(prefix="/v1-FB", tags=["Facebook"])


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError


@fb_router.post('/fetch-fb-posts')
async def fetch_fb_post(request: CrawlerSchema):
    try:
        post_data = get_fb_posts(username=request.username, days=request.days)
        if post_data:
            try:
                fb_collection.insert_many(post_data)
                return JSONResponse(content={"message": f"{request.days} posts have been saved to Database"},
                                    status_code=200)
            except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
                return JSONResponse(
                    content={"Error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "Details": str(db_error)}, status_code=500)
        else:
            return JSONResponse(content={"Message": "Scraping Failed"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"Error": str(e)}, status_code=500)
