#!/usr/bin/env python3

#Libs
import csv
import rospy

#Messages
from niryo_robot_msgs.msg import HardwareStatus
from sensor_msgs.msg import JointState

# Initialize lists for data collection
temp = []
pos = []
load = []

# Callback for hardware status
def callback_HS(data):
    temp.append(data.temperature)
    load.append(data.load)

# Callback for joint state
def callback_JS(data):
    pos.append(data.position)

# Save data to CSV
def save_to_csv():
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Temperature", "Position", "Load"])
        # Iterate over the longest list and handle missing data
        max_length = max(len(temp), len(pos), len(load))
        for i in range(max_length):
            row = [
                temp[i] if i < len(temp) else None,
                pos[i] if i < len(pos) else None,
                load[i] if i < len(load) else None
            ]
            writer.writerow(row)
    rospy.loginfo("Data saved to data.csv")

# Listener setup and shutdown handling
def listener():
    rospy.init_node('data_collection', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, callback_HS)
    rospy.Subscriber("/joint_states", JointState, callback_JS)
    
    # Register the save_to_csv function to be called upon node shutdown
    rospy.on_shutdown(save_to_csv)
    
    rospy.spin()  # Keep the node running until interrupted

if __name__ == '__main__':
    listener()
