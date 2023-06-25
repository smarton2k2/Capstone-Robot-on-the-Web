from azure.iot.device import IoTHubDeviceClient, Message  #version 2.5.1
import json
device_connection_string = "HostName=NiryoIOTServer.azure-devices.net;DeviceId=Test_hari_device;SharedAccessKey=HMlcN6pZ7RzGIIfwkrIjM2Q0SDGEdjEI/X/3PQtAKoY="

device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()
positions = [-0.0007288597570993538, 0.49940895727663126, -1.2506181983468665,
 9.265358979293481e-05, -0.0031606151655640957, 0.0016266343776782932]
message = Message(json.dumps(positions))
device_client.send_message(message)
device_client.disconnect()