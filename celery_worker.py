import json
import pika
from models import db, Item
from config import Config
from tasks import celery_app, process_item_task
from flask import Flask
from config import Config as AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        item_id = data.get('item_id')
        item_name = data.get('item')
        print(f"Received: {data}")
        
        with app.app_context():
            item = Item.query.get(item_id)
            if item:
                item.status = 'completed'
                db.session.commit()
                print(f"Updated item {item_id} to completed")
            else:
                print(f" Item {item_id} not found")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def start_consumer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=Config.RABBITMQ_HOST)
        )
        channel = connection.channel()
        channel.queue_declare(queue=Config.RABBITMQ_QUEUE, durable=True)
        channel.basic_qos(prefetch_count=1)
        
        channel.basic_consume(
            queue=Config.RABBITMQ_QUEUE,
            on_message_callback=callback
        )
        
        print(f"Waiting for messages in queue: {Config.RABBITMQ_QUEUE}")
        print("Press CTRL+C to stop")
        
        channel.start_consuming()
        
    except Exception as e:
        print(f"Error starting consumer: {e}")
        raise


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    start_consumer()