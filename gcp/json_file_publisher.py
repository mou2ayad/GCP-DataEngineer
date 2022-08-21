import json
from google.cloud import pubsub_v1

crd_file='/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json'


publisher = pubsub_v1.PublisherClient.from_service_account_json(crd_file)
topic_path = 'projects/zeta-period-359422/topics/dataeng_assignment'


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def publishFilesToPubSub(directory,files):
    for file in files:
        with open(directory + '/' + file) as inputFile:
            for line in inputFile:
                if validateJSON(line):
                    data = line.encode('utf-8')
                    publisher.publish(topic_path, data)
                else:
                    print(f'invalid json {line}')
    return True

# files = ['yc_app_events_2022_05_31.json','yc_app_events_2022_06_02.json','yc_app_events_2022_06_01.json']
files = ['yc_app_events_2022_06_01.json']

directory='/Users/mouayadkhashfeh/Downloads'

publishFilesToPubSub(directory,files)
