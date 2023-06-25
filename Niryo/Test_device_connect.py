from azure.iot.device import IoTHubDeviceClient, Message  #version 2.5.1

device_connection_string = "HostName=NiryoIOTServer.azure-devices.net;DeviceId=Test_hari_device;SharedAccessKey=HMlcN6pZ7RzGIIfwkrIjM2Q0SDGEdjEI/X/3PQtAKoY="

device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()
positions = "x = 0.3, y = 0, z = 0, roll = -0.1, pitch = 0.1, yaw = -0.05"
message = Message(positions)
device_client.send_message(message)
device_client.disconnect()