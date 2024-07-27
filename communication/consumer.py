from communication.rabbitmq import RabbitMQConnection, callback

# Use the RabbitMQConnection class to consume messages
with RabbitMQConnection() as rabbitmq:
    rabbitmq.consume(callback)
