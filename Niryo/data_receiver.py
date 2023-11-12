from flask import Flask, jsonify
from azure.iot.device import IoTHubDeviceClient
import threading
import json
import sys

device_connection_string = "HostName=niryoiot.azure-devices.net;DeviceId=NiryoNed2;SharedAccessKey=Ee0uclVHdESQI+NPmG8z5G3ZA1ET0dkpiZ5lbyOY4Oo=="

latest_data = None

app = Flask(__name__)

@app.route('/get_data')
def get_data():
    if latest_data:
        return jsonify(latest_data)
    return jsonify({"error": "No data received yet."})

def azure_data_receiver():
    global latest_data
    client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

    def message_handler(message):
        global latest_data
        latest_data = message.data.decode('utf-8')
        print("Received data: " + latest_data)

    try:
        client.on_message_received = message_handler
        client.connect()
        while True:
            continue
    except KeyboardInterrupt:
        print("Stopped receiving.")
        client.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    azure_thread = threading.Thread(target=azure_data_receiver)
    azure_thread.start()
    app.run(port=5000)
