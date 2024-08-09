import pprint
from fastapi import APIRouter
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from starlette.responses import JSONResponse

from communication.rabbitmq import RabbitMQConnection
from database.queries import get_all_users, add_user_to_db, get_user_by_id, get_user_by_email, \
    get_user_by_id_extend_posts, delete_user_by_id
from schemas import UserSchema
from utils import serialize_object_id

route = APIRouter(prefix="/user", tags=["Users"])


@route.post('/add-user')
async def add_user(request: UserSchema):
    user_data = request.as_dict()

    # Check if the user already exists
    existing_user = get_user_by_email(user_data['email'])
    if existing_user:
        return JSONResponse(
            content={"message": f'User already exists with ID: {existing_user.get("_id")}'},
            status_code=200
        )

    try:
        # Add user to the database
        user_id = add_user_to_db(user_data)
        if user_id:
            # Publish message to RabbitMQ
            try:
                with RabbitMQConnection() as rabbitmq:
                    rabbitmq.publish(serialize_object_id(user_data))
                    print("Message published to the queue")
            except Exception as rabbitmq_error:
                return JSONResponse(
                    content={"error": "Failed to publish message to RabbitMQ.", "details": str(rabbitmq_error)},
                    status_code=500
                )

            return JSONResponse(
                content={"message": f"Crawling started for {user_data['name']} based on its queue number.",
                         'user_id': serialize_object_id(user_id)},
                status_code=200
            )
    except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
        return JSONResponse(
            content={"error": "Database connection error. Ensure MongoDB is running.", "details": str(db_error)},
            status_code=500
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@route.get('/get-by-id')
async def get_user(user_id: str):
    user = get_user_by_id(user_id)
    if user:
        return JSONResponse(
            content=serialize_object_id(user),
            status_code=200
        )
    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )


@route.delete('/delete-by-id')
async def delete_user(user_id: str):
    user = delete_user_by_id(user_id)
    if user:
        return JSONResponse(
            content=user,
            status_code=200
        )
    return JSONResponse(
        content={"message": "User not found. Check if MongoDB is running."},
        status_code=404
    )


@route.get('/get-users')
async def get_users():
    try:
        users = get_all_users()
        serialized_users = serialize_object_id(users)
        if serialized_users:
            return JSONResponse(
                content=serialized_users,
                status_code=200
            )
        return JSONResponse(
            content={"message": "No users found. Please add users."},
            status_code=404
        )
    except (ServerSelectionTimeoutError, ConnectionFailure) as db_error:
        return JSONResponse(
            content={"error": "Database connection error. Ensure MongoDB is running.", "details": str(db_error)},
            status_code=500
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )
