import pyniryo
from azure.iot.device import IoTHubDeviceClient, Message  #version 2.5.1
import json

device_connection_string = "HostName=NiryoIOTServer.azure-devices.net;DeviceId=Niryo_Robot;SharedAccessKey=H0BXq3Dz1iEZmcBy2UUoewHO/p8R4sWcm7OOR+feMjI="

device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()

data = pyniryo.Robot.get_joints()
message = Message(json.dump(data))
device_client.send_message(message)
device_client.disconnect()