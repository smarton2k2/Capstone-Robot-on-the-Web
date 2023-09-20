from azure.iot.device import IoTHubDeviceClient, Message
import json

try:
    device_connection_string = "HostName=Niryo.azure-devices.net;DeviceId=Niryo_Ned2;SharedAccessKey=SJaVvz+aGzioqBeIHg7Wj3zci0T1E683rNoYzPFQGPk="

    device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
    device_client.connect()
    # positions = [0.12312313712, 0.012312313, 0.1414514214, 1.123123131, 0, 0.0031412]
    positions = [0, 0, 0, 0, 0, 0]
    message = Message(json.dumps(positions))
    device_client.send_message(message)
    
finally:
    device_client.disconnect()
