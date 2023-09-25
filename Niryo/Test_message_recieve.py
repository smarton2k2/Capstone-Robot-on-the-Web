from azure.eventhub import EventHubConsumerClient
from pyniryo import *
import ast

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodpnres017dednamespace.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-niryoiot-25263541-af3f4ab300"
IOTHUB_SAS_KEY = "JCqKnk2r6LzjU3QQyd74eGLHneplSDlHmAIoTHWhsic="
SHARED_ACCESS_KEY_NAME = "iothubowner"


robot_ip_address = "169.254.200.200"
robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()

def get_eventhub_credentials():
    return {
        'endpoint': EVENTHUB_COMPATIBLE_ENDPOINT,
        'path': EVENTHUB_COMPATIBLE_PATH,
        'sas_key': IOTHUB_SAS_KEY,
        'shared_access_key_name': SHARED_ACCESS_KEY_NAME
    }

def on_event_batch(partition_context, events):
    for event in events:
        print(f"Received event from partition: {partition_context.partition_id}.")
        x = event.body_as_str()
        lst = ast.literal_eval(x)
        print(f"Telemetry received: {lst}")
        robot.move_joints(lst[0], lst[1], lst[2], lst[3], lst[4], lst[5])
    partition_context.update_checkpoint()

def main():
    credentials = get_eventhub_credentials()

    try:
        connection_str = (f"Endpoint={credentials['endpoint']};"
                          f"SharedAccessKeyName={credentials['shared_access_key_name']};"
                          f"SharedAccessKey={credentials['sas_key']};"
                          f"EntityPath={credentials['path']}")

        client = EventHubConsumerClient.from_connection_string(
            connection_str,
            consumer_group="$Default",
        )

        print("Listening for messages. Press CTRL+C to stop.")
        with client:
            client.receive_batch(on_event_batch, starting_position="-1")
    
    except KeyboardInterrupt:
        print("Stopping the listener.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()