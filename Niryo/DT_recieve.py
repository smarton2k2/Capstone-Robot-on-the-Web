from flask import Flask, jsonify
from azure.eventhub import EventHubConsumerClient
import threading

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodpnres017dednamespace.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-niryoiot-25263541-af3f4ab300"
IOTHUB_SAS_KEY = "JCqKnk2r6LzjU3QQyd74eGLHneplSDlHmAIoTHWhsic="
SHARED_ACCESS_KEY_NAME = "iothubowner"

latest_data = ""

app = Flask(__name__)

@app.route('/get_data')
def get_data():
    if latest_data:
        return jsonify({"data": latest_data})
    return jsonify({"error": "No data received yet."})

def azure_data_receiver(partition_context, data_set):
    global latest_data
    for data in events:
        latest_data = data.body_as_str()
        print("Received data: " + latest_data)
    partition_context.update_checkpoint()

def azure_receiver():
    client = EventHubConsumerClient.from_connection_string(
        "Endpoint=" + EVENTHUB_COMPATIBLE_ENDPOINT + ";SharedAccessKeyName=" + SHARED_ACCESS_KEY_NAME + ";SharedAccessKey=" + IOTHUB_SAS_KEY + ";EntityPath=" + EVENTHUB_COMPATIBLE_PATH,
        consumer_group="$Default",
    )
    try:
        with client:
            client.receive_batch(azure_data_receiver, starting_position="-1")
    except KeyboardInterrupt:
        print("Stopped receiving.")

if __name__ == '__main__':
    azure_thread = threading.Thread(target=azure_receiver)
    azure_thread.start()
    app.run(port=5000)