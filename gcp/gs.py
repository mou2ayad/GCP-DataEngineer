def implicit():
    from google.cloud import storage

    storage_client = storage.Client()

    buckets = list(storage_client.list_buckets())
    print(buckets)

def explicit():
    from google.cloud import storage

   
    storage_client = storage.Client.from_service_account_json(
        '/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json')

    
    buckets = list(storage_client.list_buckets())
    print(buckets)

explicit()