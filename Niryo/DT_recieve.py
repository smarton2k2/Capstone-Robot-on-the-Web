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
    return jsonify({"Current location": latest_data})

def on_event_batch(partition_context, events):
    global latest_data
    for event in events:
        latest_data = event.body_as_str()
    partition_context.update_checkpoint()

def azure_listener():
    client = EventHubConsumerClient.from_connection_string(
        "Endpoint=" + EVENTHUB_COMPATIBLE_ENDPOINT + ";SharedAccessKeyName=" + SHARED_ACCESS_KEY_NAME + ";SharedAccessKey=" + IOTHUB_SAS_KEY + ";EntityPath=" + EVENTHUB_COMPATIBLE_PATH,
        consumer_group="$Default",
    )
    try:
        with client:
            client.receive_batch(on_event_batch, starting_position="-1")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    azure_thread = threading.Thread(target=azure_listener)
    azure_thread.start()
    app.run(port=5000, debug=True)