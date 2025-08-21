# app/data_producer.py
import threading
import time
import random
from queue_handler import data_queue


def data_producer():
    while True:
        data_point = {
            "timestamp": time.time(),
            # Replace with telemetry or market data
            "value": random.uniform(0, 100)
        }
        # print("Producing data:", data_point)
        data_queue.put(data_point)
        time.sleep(0.1)  # Simulate fast updates (10 Hz)


def start_producer():
    thread = threading.Thread(target=data_producer, daemon=True)
    thread.start()
