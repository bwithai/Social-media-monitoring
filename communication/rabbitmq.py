import json
import os
import pprint

import pika

from FB.get_posts import get_fb_posts
from X.get_tweets import get_tweets
from database.queries import add_crawler_data, add_logs
from schemas import CrawlerSchema


# Context manager class
class RabbitMQConnection:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.username = os.getenv("RABBITMQ_USERNAME", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.queue_name = "user_queue"

    def __enter__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(username=self.username, password=self.password)
            )
        )
        self.channel = self.connection.channel()
        return self

    def publish(self, payload: dict):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)  # pika.spec.PERSISTENT_DELIVERY_MODE
        )

    def consume(self, callback):
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        print('Starting to consume...')
        self.channel.start_consuming()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('closing the connection')
        self.connection.close()


# Callback function to process the messages
def callback(ch, method, properties, body):
    print("Received message:")
    user = json.loads(body)
    start_crawling(user)


def start_crawling(user):
    def crawl(platform, username, days, crawler, email, get_posts_func):
        logs = ""
        try:
            logs += f"{platform} \n"
            request = CrawlerSchema(username=username, days=days)
            data = get_posts_func(username=request.username, days=request.days)
            if data:
                result = add_crawler_data(request, data, crawler, email)
                if isinstance(result, Exception):
                    logs += f"\t- Error: Failed to connect to MongoDB for {crawler}.\n"
                    logs += f"\t- Details: {str(result)}\n"
                else:
                    logs += f"\t- Message: {result}\n"
            else:
                logs += f"\t- Message: {crawler} Scraping Failed\n"
        except Exception as e:
            logs += f"\t- Error: {str(e)}\n"

        add_logs(email, logs)

    if user.get('fb_username'):
        crawl('Facebook', user['fb_username'], user['num_fb_posts'], 'facebook', user['email'], get_fb_posts)

    if user.get('x_username'):
        crawl('X', user['x_username'], user['num_x_days'], 'X', user['email'], get_tweets)

    # Add additional platforms as needed, e.g., Instagram
