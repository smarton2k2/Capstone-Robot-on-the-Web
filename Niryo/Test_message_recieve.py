from azure.eventhub import EventHubConsumerClient

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodpnres004dednamespace.servicebus.windows.net/"
EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-niryo-25211978-9c0160d5de"
IOTHUB_SAS_KEY = "7drXDIezuMMCtLij2eLGqTiG6q+DCF/k+AIoTHxp+Lo="
SHARED_ACCESS_KEY_NAME = "iothubowner"

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
        print(f"Telemetry received: {event.body_as_str()}")
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