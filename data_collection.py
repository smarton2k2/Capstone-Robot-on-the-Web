#!/usr/bin/env python3

import rospy
import csv
from niryo_robot_msgs.msg import HardwareStatus

# Setup CSV writer
csv_file = open('/home/smarton/capstone/temperature_voltage_data.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(["Seq", "Time Secs", "Temperatures", "Voltages"])

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
        csv_file.flush()
    except Exception as e:
        rospy.logerr("Error in callback_HS: {}".format(e))

def listener():
    rospy.init_node('data_collection_node', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, callback_HS)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        rospy.loginfo("Shutting down data collection node")
    finally:
        csv_file.close()
