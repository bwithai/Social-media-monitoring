import pprint

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from database.queries import get_all_users
from schemas import UserSchema
from database.mongo_client import user_collection
from utils import serialize_object_id

user_router = APIRouter(prefix="/v1-User", tags=["Users"])


@user_router.post('/add-user')
async def add_user(request: UserSchema):
    try:
        user = request.as_dict()
        if user:
            try:
                user_collection.insert_one(user)
                return JSONResponse(content={"message": "User has been saved to the database."},
                                    status_code=200)
            except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
                return JSONResponse(
                    content={"error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "details": str(db_error)}, status_code=500)
        else:
            return JSONResponse(content={"message": "User data is empty"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@user_router.get('/get-users')
async def get_users():
    try:
        users = serialize_object_id(get_all_users())
        return JSONResponse(content=users,
                            status_code=200)
    except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
        return JSONResponse(
            content={"error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                     "details": str(db_error)}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
