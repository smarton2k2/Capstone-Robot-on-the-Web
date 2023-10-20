from azure.iot.device import IoTHubDeviceClient, Message  #version 2.5.1
import json

device_connection_string = "HostName=niryoiot.azure-devices.net;DeviceId=NiryoNed2;SharedAccessKey=Ee0uclVHdESQI+NPmG8z5G3ZA1ET0dkpiZ5lbyOY4Oo=="

device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()

# data = "0,0,0,0,0,0,0,0,0"
data = "0, 0, 0.0007930673506395536, 0.27671192603916284, -1.0264062213186669, -0.025985019804263043, -0.263937349106123, 0.0706557698325323, 0"
message = Message(data)
device_client.send_message(message)
device_client.disconnect()