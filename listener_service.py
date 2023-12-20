import redis
import pika
import time
import sys

redis_host = 'localhost' 
rabbitmq_host = 'localhost' 

def connect_to_redis():
    retries = 5
    delay = 5
    for i in range(retries):
        try:
            r = redis.Redis(host=redis_host, port=6379, db=0)
            r.ping()
            return r
        except (redis.exceptions.ConnectionError, redis.exceptions.BusyLoadingError):
            print(f"Waiting for Redis... {i+1}/{retries}")
            time.sleep(delay)
    sys.exit("Error: Unable to connect to Redis")

def connect_to_rabbitmq():
    retries = 5
    delay = 5
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"Waiting for RabbitMQ... {i+1}/{retries}")
            time.sleep(delay)
    sys.exit("Error: Unable to connect to RabbitMQ")

redis_connection = connect_to_redis()
rabbitmq_connection = connect_to_rabbitmq()
channel = rabbitmq_connection.channel()
channel.queue_declare(queue='key_expiry_notifications')

pubsub = redis_connection.pubsub()
pubsub.psubscribe('__keyevent@0__:expired')

def listen_for_key_expiry():
    try:
        print("Listening for key expiries...")
        for message in pubsub.listen():
            if message['type'] == 'pmessage':
                expired_key = message['data'].decode('utf-8')
                print(f"Key expired: {expired_key}")
                # channel.basic_publish(exchange='',
                #                       routing_key='key_expiry_notifications',
                #                       body=f"Expired: {expired_key}")
    except KeyboardInterrupt:
        print("Interrupt received, stopping listener...")
    finally:
        pubsub.close()
        rabbitmq_connection.close()
        print("Listener stopped.")

# Start listening
listen_for_key_expiry()
