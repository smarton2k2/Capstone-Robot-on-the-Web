from azure.iot.device import IoTHubDeviceClient, Message
import json

try:
    device_connection_string = "HostName=Niryo.azure-devices.net;DeviceId=Niryo_Ned2;SharedAccessKey=SJaVvz+aGzioqBeIHg7Wj3zci0T1E683rNoYzPFQGPk="

    device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
    device_client.connect()
    positions = [0, 0, 0, 0, 0, 1]
    message = Message(json.dumps(positions))
    device_client.send_message(message)
    
finally:
    device_client.disconnect()
