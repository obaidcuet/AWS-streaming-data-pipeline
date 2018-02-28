import boto3
import json
from sseclient import SSEClient as EventSource

def put_to_stream(kinesis_client, stream_name, records):
    #print (records)
    put_response = kinesis_client.put_records(
                        StreamName= stream_name,
                        Records = records)
						
    print (put_response["ResponseMetadata"])


def start_producer(kinesis_client, stream_name, url, batch_size):

    records = []
    count_records = 0

    for event in EventSource(url):
        if event.event == 'message':
            try:
                wikichange = json.loads(event.data)
            except ValueError:
                pass
            else:
                payload = {
                    'timestamp': wikichange['timestamp'],
                    'id': wikichange['id'],
                    'type': str(wikichange['type']),
                    'wiki': str(wikichange['wiki'])
                }
                records.append({'Data': json.dumps(payload), 'PartitionKey': "filler"}) # dummy PartitionKey, as we only have one sherd
                count_records = count_records + 1

        if count_records == batch_size : # send data in a batch of 100 records
            put_to_stream(kinesis_client, stream_name, records)
            records = []
            count_records = 0


# main
if __name__ == "__main__":

    batch_size = 100
    stream_name = 'wikiedits'
    region = 'us-east-1'
    url = 'https://stream.wikimedia.org/v2/stream/recentchange'

    kinesis_client = boto3.client(
        region_name=region,al
        aws_access_key_id='<aws_access_key_id>',
        aws_secret_access_key='<aws_secret_access_key>'
    )

    start_producer(kinesis_client, stream_name, url, batch_size)

