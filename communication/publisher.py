from communication.rabitmq import RabbitMQConnection, callback

import json

# The payload to be sent to the queue
payload = {
    "video_id": "12345",
    "title": "Example Video",
    "description": "This is an example description.",
    "url": "http://example.com/video/12345"
}

# Using the RabbitMQConnection class
with RabbitMQConnection() as rabbitmq:
    rabbitmq.publish(payload)
    print("Message published to the queue")
