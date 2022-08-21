from google.cloud import pubsub_v1

crd_file='/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json'

publisher = pubsub_v1.PublisherClient.from_service_account_json(crd_file)
topic_path = 'projects/zeta-period-359422/topics/dataeng_assignment'


data = '{"uuid":"ba84f725-d150-40a3-8e60-9d4df545bfbe","created_at":"2022-05-31T23:09:17.805Z","data":{"site_id":1001},"meta":{"site_id":1001},"type":"html_vacancy_search"}'
data = data.encode('utf-8')


future = publisher.publish(topic_path, data)
print(f'published message id {future.result()}')

