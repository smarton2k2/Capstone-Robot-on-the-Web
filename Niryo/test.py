from pyniro2 import NiryoRobot
import sys

simu = "-simu" in sys.argv

robot_ip_rpi = "10.10.10.10"
robot_ip_sim = "127.0.0.1"

robot_ip = robot_ip_sim if simu else robot_ip_rpi

robot = NiryoRobot(ip_address = robot_ip)
robot.arm.calibrate_auto()
