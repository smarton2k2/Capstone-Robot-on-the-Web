#!/usr/bin/env python3

import csv
import rospy
from niryo_robot_msgs.msg import HardwareStatus
from sensor_msgs.msg import JointState

# Open the CSV file for writing
csv_file = open('temperature_voltage_data.csv', 'w', newline='')
writer = csv.writer(csv_file)

# Write the header row based on the expected message fields
header = ["Seq", "Time Secs", "Time Nsecs", "Temperatures", "Voltages"]
writer.writerow(header)

def callback_HS(data):
    # Create a list of the data fields you want to write to the CSV
    row = [
        data.header.seq,
        data.header.stamp.secs,
        data.header.stamp.nsecs,
        ';'.join(map(str, data.temperatures)),  # Convert each temperature to string and join
        ';'.join(map(str, data.voltages)),      # Convert each voltage to string and join
    ]
    
    # Write the data to the CSV and flush to ensure it's written to disk
    writer.writerow(row)
    csv_file.flush()

def listener():
    rospy.init_node('data_collection_node', anonymous=True)
    rospy.Subscriber("/niryo_robot_hardware_interface/hardware_status", HardwareStatus, callback_HS)
    rospy.spin()


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
    finally:
        csv_file.close()
