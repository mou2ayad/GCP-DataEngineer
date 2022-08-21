# Load Newline Delimited JSON files from gs to bq

1. From Cloud Shell, set the active project to (**zeta-period-359422**)

```bash
$ gcloud config set project zeta-period-359422
```

2. Create gs bucket (**yc-learning**) in **eu** region:

``` bash
$ gsutil mb -c standard -l eu gs://yc-learning
```

3. Create bq dataset in eu region

```bash
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
```bash
$ ls
```

5. Create bq table with the created dataset using the uploaded schema

```bash
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
