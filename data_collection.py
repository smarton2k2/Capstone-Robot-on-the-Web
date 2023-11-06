#!/usr/bin/env python3

import rospy
import csv
from niryo_robot_msgs.msg import HardwareStatus
from sensor_msgs.msg import JointState
import time

# Setup CSV writer
csv_file1 = open('/home/smarton/capstone/temperature_voltage_data.csv', 'w', newline='')
writer = csv.writer(csv_file1)
writer.writerow(["Seq", "Time Secs", "Temperatures", "Voltages"])

csv_file2 = open('/home/smarton/capstone/effort_position_data.csv', 'w', newline='')
writer2 = csv.writer(csv_file2)
writer2.writerow(["Seq", "Time Secs", "Effort", "Position"])

def callback_HS(data):
    try:
        rospy.loginfo("Received message on /niryo_robot_hardware_interface/hardware_status")
        row = [
            data.header.seq,
            data.header.stamp.secs,
            ';'.join(map(str, data.temperatures)),
            ';'.join(map(str, data.voltages)),
        ]
        writer.writerow(row)
        csv_file1.flush()
    except Exception as e:
        rospy.logerr("Error in callback_HS: {}".format(e))

def callback_JS(data):
    try:
        rospy.loginfo("Received message on /joint_states")
        row = [
            data.header.seq,
            data.header.stamp.secs,
            ';'.join(map(str, data.effort)),
            ';'.join(map(str, data.position)),
        ]
        writer2.writerow(row)
        csv_file2.flush()
    except Exception as e:
        rospy.logerr("Error in callback_JS: {}".format(e))

def listener():
    rospy.init_node('data_collection_node', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, callback_HS)
    rospy.Subscriber("/joint_states", JointState, callback_JS)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        rospy.loginfo("Shutting down data collection node")
    finally:
        csv_file1.close()
        csv_file2.close()