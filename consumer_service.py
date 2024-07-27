import time

from communication.rabbitmq import RabbitMQConnection, callback


def start_consume():
    while True:
        try:
            # Use the RabbitMQConnection class to consume messages
            with RabbitMQConnection() as rabbitmq:
                rabbitmq.consume(callback)
        except Exception as rabbitmq_error:
            print("Failed to consume from RabbitMQ.", "\ndetails: ", str(rabbitmq_error))
            time.sleep(5)  # Wait for 5 seconds before retrying


# Entry point to start consuming messages
if __name__ == "__main__":
    start_consume()
