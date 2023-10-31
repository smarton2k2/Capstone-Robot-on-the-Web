import rospy
from pyniryo import *

robot_ip_address = "10.10.10.10"

class NiryoNedInterface:
    def __init__(self):
        self.robot = NiryoRobot(robot_ip_address)
        
    def move_joint(self, joint_angles):
        self.robot.move_joints(joint_angles)

    def get_status(self):
        return self.robot.get_status()
