import pprint

from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from communication.rabbitmq import RabbitMQConnection
from database.queries import get_all_users, add_user_to_db, get_user_by_id
from schemas import UserSchema
from utils import serialize_object_id

router = APIRouter(prefix="/v1-User", tags=["Users"])


@router.post('/add-user')
async def add_user(request: UserSchema):
    try:
        user = request.as_dict()
        pprint.pprint(user)
        if user:
            try:
                user_id = add_user_to_db(user)
                if user_id:
                    try:
                        with RabbitMQConnection() as rabbitmq:
                            rabbitmq.publish(request.as_dict())
                            print("Message published to the queue")
                    except Exception as rabbitmq_error:
                        return JSONResponse(
                            content={"error": "Failed to publish to RabbitMQ.", "details": str(rabbitmq_error)},
                            status_code=500
                        )

                    return JSONResponse(content={"message": f"Crawling started for {user['name']} based on its queue.",
                                                 'user_id': user_id},
                                        status_code=200)
            except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
                return JSONResponse(
                    content={"error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                             "details": str(db_error)}, status_code=500)
        else:
            return JSONResponse(content={"message": "User data is empty"}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.get('/get-by-id')
async def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return JSONResponse(content=user, status_code=200)
    else:
        return JSONResponse(content={"message": "User not found. does mongodb docker started"}, status_code=200)


@router.get('/get-users')
async def get_users():
    try:
        users = serialize_object_id(get_all_users())
        if users:
            return JSONResponse(content=users, status_code=200)
        else:
            return JSONResponse(content={"message": "Please add user"}, status_code=200)
    except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
        return JSONResponse(
            content={"error": "Failed to connect to MongoDB. Please ensure MongoDB Docker is running.",
                     "details": str(db_error)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
