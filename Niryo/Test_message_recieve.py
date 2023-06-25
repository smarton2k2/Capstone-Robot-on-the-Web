from azure.eventhub import EventHubConsumerClient

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://iothub-ns-niryoiotse-25113370-d460bcb1a9.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "niryoiotserver"
IOTHUB_SAS_KEY = "kkPgceuCkkNDarQ0Y5HMuz9NlMI+tcDC/qwNUosKNdQ="
SHARED_ACCESS_KEY_NAME = "test_niryo"

def on_event_batch(partition_context, events):
    for event in events:
        print("Received event from partition: {}.".format(partition_context.partition_id))
        print("Telemetry received: ", event.body_as_str())
    partition_context.update_checkpoint()

client = EventHubConsumerClient.from_connection_string(
    "Endpoint=" + EVENTHUB_COMPATIBLE_ENDPOINT + ";SharedAccessKeyName=" + SHARED_ACCESS_KEY_NAME + ";SharedAccessKey=" + IOTHUB_SAS_KEY + ";EntityPath=" + EVENTHUB_COMPATIBLE_PATH,
    consumer_group="$Default",
)

with client:
    client.receive_batch(on_event_batch, starting_position="-1")
