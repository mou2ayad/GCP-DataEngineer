# Load Newline Delimited JSON files from gs to bq

1. From Cloud Shell, set the active project to (**zeta-period-359422**)

``` shell
$ gcloud config set project zeta-period-359422
```

2. Create gs bucket (**yc-learning**) in **eu** region:

``` shell
$ gsutil mb -c standard -l eu gs://yc-learning
```

3. Create bq dataset in eu region

``` shell
$ bq mk --location=eu bq_dataeng_assignment
```

4. Upload [yc-events-schema.json](yc-events-schema.json) to Cloud shell

```json
{ 
   "BigQuery Schema": [
      {
         "name":"uuid",
         "type":"STRING",
         "mode":"REQUIRED"
      },
      {
         "name":"created_at",
         "type":"TIMESTAMP",
         "mode":"REQUIRED"
      },
      {
         "name":"data",
         "type":"JSON",
         "mode":"NULLABLE"
      },
      {
         "name":"meta",
         "type":"JSON",
         "mode":"NULLABLE"
      },
      {
         "name":"type",
         "type":"STRING",
         "mode":"REQUIRED"
      }
   ]
}
```

You can check the file after uploading to the cli using:
``` shell
$ ls
```

5. Create bq table (**yc_app_events_bq**) with the created dataset using the uploaded schema

``` shell
$ bq mk   -t   --expiration 0 /
  -- description "This is my yc apps events table" /
  bq_dataeng_assignment.yc_app_events_bq /
  ./yc-events-schema.json

```

6. Execute [cleanJsonFiles.py](cleanJsonFiles.py) python script in the local machine to exclude the corrupted JSON lines from the files (we can run the file using gcp cli directly but the code needs to be changed a little bit to use gs API)

``` python
import json

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True

def cleanJSONFile(jsonFilePath,cleanFilePath,dirtyFilePath):
    with open(jsonFilePath) as inputFile, open(cleanFilePath, 'w') as cf, open(dirtyFilePath, 'w') as df:
        for line in inputFile:
            if validateJSON(line):
                cf.write(line)
            else:
                df.write(line)
    return True

def cleanJsonFiles(directory,files):
    for file in files:
        cleanFilePath = directory + '/' + file.split('.')[0] + '_clean.json'
        dirtyFilePath = directory + '/' + file.split('.')[0] + '_dirty.json'
        cleanJSONFile(directory + '/' + file,cleanFilePath,dirtyFilePath)
    return True

files = ['yc_app_events_2022_05_31.json','yc_app_events_2022_06_02.json','yc_app_events_2022_06_01.json']

directory='/Users/mouayadkhashfeh/Downloads'

cleanJsonFiles(directory,files)



```

7. Upload the clean files created by running the code above to gs bucket under this folder **gs://yc-learning/yc-test/clean**

8. Execute this query in bq to load the data from gs files to bq table

``` sql

LOAD DATA into `zeta-period-359422.bq_dataeng_assignment.yc_app_events_bq`
FROM FILES (
 ignore_unknown_values=true,
 format = 'JSON',
 uris = [
   'gs://yc-learning/yc-test/yc_app_events_2022_06_01_clean.json'
   ,'gs://yc-learning/yc-test/clean/yc_app_events_2022_05_31_clean.json'
   ,'gs://yc-learning/yc-test/clean/yc_app_events_2022_06_02_clean.json'
   ])

```


## Transform data from pub/sub to bigquery

1. Create bq table (**yc_app_events_bq_pubsub**) from **yc-events-schema**, or skip this step if you want to use the same table we created before (**yc_app_events_bq**)

``` shell
bq mk   -t   --expiration 0  /
 --description "This is my yc apps events table for 
 PubSub messages" /
 bq_dataeng_assignment.yc_app_events_bq_pubsub /
 ./yc-events-schema.json
```

2. Create pub/sub topic **dataeng_assignment**

``` shell
$ gcloud pubsub topics create dataeng_assignment
```

2- Upload [transform_pubsub.js](transform_pubsub.js) to gs bucket **gs://yc-learning**, this file helps to exclude the invalid json lines 

``` js
function transform(input) {
  try {  
     jsonObject = JSON.parse(input); 
     output={}
     output.uuid=jsonObject.uuid
     output.created_at=jsonObject.created_at
     output.data=JSON.stringify(jsonObject.data)
     output.meta=JSON.stringify(jsonObject.meta)
     output.type=jsonObject.type
    return JSON.stringify(output);
  } catch (e) {  }
}
```

3- Execute this command to create and run dataflow pipeline, from pub/sub topic to bq:

``` shell

$ gcloud dataflow jobs run transfer_yc_app_events_pipeline \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --region europe-west4 \
    --staging-location gs://yc-learning/dataflow/staging/temp \
    --parameters \
      inputTopic=projects/zeta-period-359422/topics/dataeng_assignment,\
      outputTableSpec=zeta-period-359422:bq_dataeng_assignment.yc_app_events_bq_pubsub,\
      javascriptTextTransformGcsPath=gs://yc-learning/transform_pubsub.js,\
      javascriptTextTransformFunctionName=transform

```
## Testing the created pipeline:

these python scripts can be executed in the local machine or in Cloud Shell, to run it from local machine we need to create IAM user with needed permission to publish the message to pub/sub and create a credential key and download the credential key and add it to the code as follows 

### 1.Creating publisher to publish a single message to pub/sub:

the script is added to [publisher.py](gcp/publisher.py)

``` python
from google.cloud import pubsub_v1

crd_file='/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json'

publisher = pubsub_v1.PublisherClient.from_service_account_json(crd_file)
topic_path = 'projects/zeta-period-359422/topics/dataeng_assignment'


data = '{"uuid":"ba84f725-d150-40a3-8e60-9d4df545bfbe","created_at":"2022-05-31T23:09:17.805Z","data":{"site_id":1001},"meta":{"site_id":1001},"type":"html_vacancy_search"}'
data = data.encode('utf-8')


future = publisher.publish(topic_path, data)
print(f'published message id {future.result()}')


```

### 2. Creating publisher to publish Newline Delimited Json lines to the pub/sub:

the script is added to [json_file_publisher.py](gcp/json_file_publisher.py)

``` python
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

files = ['yc_app_events_2022_06_01.json']

directory='/Users/mouayadkhashfeh/Downloads'

publishFilesToPubSub(directory,files)

```

### [Here](metrics/README.md) is metrics documentation 
