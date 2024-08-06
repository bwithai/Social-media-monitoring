import os

from fastapi import APIRouter
from starlette.responses import JSONResponse, FileResponse

import database
from database.queries import get_all_hashtags, get_user_by_id
from schemas import GraphSchema
from utils import find_severity_score

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.get('/get-pdf')
async def get_pdf(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        # Get the path to the 'database' module directory
        module_path = os.path.dirname(database.__file__)

        # Construct the path to 'pdf_db' directory
        pdf_db_path = os.path.join(module_path, 'pdf_db')

        return FileResponse(f"{pdf_db_path}/{user_id}.pdf", media_type='application/pdf', filename='file.pdf')
    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )


@router.get('/graph-data')
async def get_graph_data(tweets_id: str = None, fb_posts_id: str = None):
    x_hashtags, fb_hashtags = get_all_hashtags(tweets_id=tweets_id, fb_posts_id=fb_posts_id)

    response = {'x': {'matched': 0}, 'fb': {'matched': 0}}

    x_target_hashtags = ['palestine', 'gaza']
    fb_target_hashtags = ['fight', 'dreamers']

    if x_hashtags:
        for keyword in x_target_hashtags:
            severity_score, filtered_hashtags, percentage = find_severity_score(x_hashtags, keyword)
            response['x']['matched'] += severity_score

        response['x']['unmatched'] = len(x_hashtags) - severity_score

    if fb_hashtags:
        for keyword in fb_target_hashtags:
            severity_score, filtered_hashtags, percentage = find_severity_score(fb_hashtags, keyword)
            response['fb']['matched'] += severity_score

        response['fb']['unmatched'] = len(fb_hashtags) - severity_score

    if any(response.values()):
        return JSONResponse(content=response, status_code=200)

    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )
