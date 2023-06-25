import pyniryo
import numpy as np
import time
from  azure.eventhub import EventHubConsumerClient

robot_ip_address = "169.254.200.200"

robot = pyniryo.NiryoRobot(robot_ip_address)
robot.calibrate_auto()
robot.move_to_home_pose()

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://iothub-ns-niryoiotse-25113370-d460bcb1a9.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "niryoiotserver"
IOTHUB_SAS_KEY = "Qn1JrI3rIHIci3JJo9KqjICugOdNx6MQncVLvnYoSmA="
SHARED_ACCESS_KEY_NAME="Niryo_robot"

def on_event_batch(partition_context, events):
    for event in events:
        print(event.body_as_str())
    partition_context.update_checkpoint()

client = EventHubConsumerClient.from_connection_string(
    "Endpoint=" + EVENTHUB_COMPATIBLE_ENDPOINT + ";SharedAccessKeyName=" + SHARED_ACCESS_KEY_NAME + ";SharedAccessKey=" + IOTHUB_SAS_KEY + ";EntityPath=" + EVENTHUB_COMPATIBLE_PATH,
    consumer_group="$Default",
)

with client:
    x = client.receive_batch(on_event_batch, starting_position="-1")
