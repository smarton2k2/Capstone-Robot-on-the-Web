import rospy
from std_msgs.msg import String
from niryo_ned_wrapper import NiryoNedInterface

def command_callback(msg):
    robot.move_joint(msg.data)

if __name__ == '__main__':
    rospy.init_node('niryo_ned_node')
    robot = NiryoNedInterface()

    rospy.Subscriber("/niryo_command", String, command_callback)

    # Main ROS loop
    while not rospy.is_shutdown():
        status = robot.get_status()
        rospy.sleep(1)
