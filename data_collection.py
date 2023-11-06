#!/usr/bin/env python3

#Libs
import csv
import numpy
import rospy

#Messages
from niryo_robot_msgs.msg import HardwareStatus
from sensor_msgs.msg import JointState

#making code to collect data(Temperature, Position, Load) from niryo ned 2 via ros and then save it to csv file
#Path: data_collection.py

temp = []
pos = []
load = []


def callback_HS(data):
    temp.append(data.temperature)
    load.append(data.load)

def callback(data):
    pos.append(data.position)

def listener():
    rospy.init_node('data_collection', anonymous=True)
    hardware = rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, callback_HS)
    rospy.Subscriber("/joint_states", JointState, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature", "Position", "Load"])
        for i in range(len(temp)):
            writer.writerow([temp[i], pos[i], load[i]])