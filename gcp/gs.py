def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        '/Users/mouayadkhashfeh/Downloads/zeta-period-359422-95e8368cd3ce.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

explicit()