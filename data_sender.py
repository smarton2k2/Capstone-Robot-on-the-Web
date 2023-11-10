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


def __callback_hs(data):
    global combined_data
    try:
        rospy.loginfo("Received message on /niryo_robot_hardware_interface/hardware_status")
        x = {
            "temperatures": data.temperatures,
            "voltages": data.voltages,
        }
        device_client.send_message(str(x))
    except Exception as e:
        rospy.logerr("Error in callback: {}".format(e))

def __callback_js(data):
    try:
        rospy.loginfo("Received message on /joint_states")
        x = {
            "effort": data.effort, 
            "position": data.position
        }
        device_client.send_message(str(x))
    except Exception as e:
        rospy.logerr("Error in callback: {}".format(e))

def listener():
    rospy.init_node('data_sender_node', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, __callback_hs)
    rospy.Subscriber("/joint_states", JointState, __callback_js)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        rate.sleep()
    rospy.spin()

if __name__ == "__main__":
    listener()