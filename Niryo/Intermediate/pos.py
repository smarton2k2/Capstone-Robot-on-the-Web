import rospy
import ros_numpy
from niryo_ned2_driver.msg import JointState
from azure.iot.device import IoTHubDeviceClient, Message

connection_String = "HostName=Niryo.azure-devices.net;DeviceId=Niryo_Ned2;SharedAccessKey=SJaVvz+aGzioqBeIHg7Wj3zci0T1E683rNoYzPFQGPk="

client = IoTHubDeviceClient.create_from_connection_string(connection_String)

def joint_states_callback(msg):
    joint_states_json = ros_numpy.msg_to_json(msg)

    message = Message(joint_states_json)

    client.send_message(message)

rospy.Subscriber('/niryo_ned2/joint_states', JointState, joint_states_callback)

rospy.spin()