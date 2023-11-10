#!/usr/bin/env python3

import rospy
from azure.iot.device import IoTHubDeviceClient, Message
from niryo_robot_msgs.msg import HardwareStatus
from sensor_msgs.msg import JointState
import time
import json
import threading

device_connection_string = "HostName=niryoiot.azure-devices.net;DeviceId=NiryoNed2;SharedAccessKey=Ee0uclVHdESQI+NPmG8z5G3ZA1ET0dkpiZ5lbyOY4Oo=="
device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)
device_client.connect()

combined_data = {}
data_lock = threading.Lock()
last_update = 0

def __callback_hs(data):
    try:
        update_data("hardware_status", {"temperatures": data.temperatures, "voltages": data.voltages})
    except Exception as e:
        rospy.logerr("Error in callback: {}".format(e))

def __callback_js(data):
    try:
        update_data("joint_states", {"effort": data.effort, "position": data.position})
    except Exception as e:
        rospy.logerr("Error in callback: {}".format(e))

def update_data(key, value):
    global combined_data, last_update_time
    with data_lock:
        combined_data[key] = value
        last_update_time = time.time()

def send_data():
    global combined_data, last_update_time
    send_interval = 0.5
    while not rospy.is_shutdown():
        time.sleep(send_interval)
        with data_lock:
            if time.time() - last_update_time < send_interval:
                try:
                    device_client.send_message(json.dumps(combined_data))
                    rospy.loginfo("Sent data to Azure: {}".format(combined_data))
                except Exception as e:
                    rospy.logerr("Error sending data to Azure: {}".format(e))

def listener():
    rospy.init_node('data_sender_node', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, __callback_hs)
    rospy.Subscriber("/joint_states", JointState, __callback_js)

    send_thread = threading.Thread(target=send_data)
    send_thread.start()

    rospy.spin()

if __name__ == "__main__":
    listener()