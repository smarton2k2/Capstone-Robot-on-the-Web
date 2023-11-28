from flask import Flask, jsonify
from azure.eventhub import EventHubConsumerClient
import threading
import json
import sys
from azure.iot.device import IoTHubDeviceClient, Message

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodpnres017dednamespace.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-niryoiot-25263541-af3f4ab300"
IOTHUB_SAS_KEY = "JCqKnk2r6LzjU3QQyd74eGLHneplSDlHmAIoTHWhsic="
SHARED_ACCESS_KEY_NAME = "iothubowner"

device_connection_string = "HostName=niryoiot.azure-devices.net;DeviceId=NiryoNed2;SharedAccessKey=Ee0uclVHdESQI+NPmG8z5G3ZA1ET0dkpiZ5lbyOY4Oo=="
device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()

latest_data = None

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    if latest_data:
        return latest_data
    return jsonify({"error": "No data received yet."})

@app.route('/your-endpoint', methods=['POST'])
def receive_data_from_unity():
    try:
        data = request.json
        print("Received data from Unity:", data)
        device_client.send_message(json.dumps(data))
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"failed": e}), 500

def azure_data_receiver(partition_context, data_set):
    global latest_data
    for data in data_set:
        latest_data = data.body_as_str()
        latest_data = json.loads(latest_data)
        # print(latest_data["position"])
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
        sys.exit(1)

if __name__ == '__main__':
    azure_thread = threading.Thread(target=azure_receiver)
    azure_thread.start()
    app.run(port=5000)