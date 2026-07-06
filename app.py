import json
import time
import threading
import requests
from flask import Flask, request, jsonify
from models import db, Item
from config import Config
import pika

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["POST"])
def create_item():
    try:
        data = request.get_json()
        
        if not data or 'item' not in data:
            return jsonify({"error": "Missing 'item' field"}), 400
        
        item_name = data['item']
    
        item = Item(item=item_name, status='pending')
        db.session.add(item)
        db.session.commit()
        
        process_item_task.delay(item.id, item.item)
        
        return jsonify({
            "message": "Item accepted for processing",
            "id": item.id,
            "item": item_name,
            "status": "pending"
        }), 202
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def make_request(delay_value):
    """Make a GET request to httpbin with delay"""
    try:
        url = f"https://httpbin.org/delay/{delay_value}"
        response = requests.get(url, timeout=delay_value + 5)
        return response.status_code == 200
    except Exception as e:
        print(f"Request failed: {e}")
        return False


@app.route("/delay", methods=["GET"])
def process_concurrent_requests():
    """
    Endpoint: GET /?delay_value=2
    Makes 5 concurrent requests to httpbin.org/delay/{delay_value}
    """
    try:
        delay_value = request.args.get('delay_value')
        
        if not delay_value:
            return jsonify({"error": "Missing 'delay_value' parameter"}), 400
        
        try:
            delay_value = int(delay_value)
        except ValueError:
            return jsonify({"error": "delay_value must be an integer"}), 400
        

        start_time = time.time()
        

        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request, args=(delay_value,))
            threads.append(thread)
            thread.start()
        

        for thread in threads:
            thread.join()
        

        time_taken = time.time() - start_time
        
        return jsonify({
            "time_taken": round(time_taken, 2),
            "delay_value": delay_value,
            "requests_made": 5
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
