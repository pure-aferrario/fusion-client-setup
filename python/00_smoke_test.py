from __future__ import print_function
import fusion
from fusion.rest import ApiException
from pprint import pprint
from os import getenv

def smoke_test():
    # Configure OAuth2 access token for authorization
    configuration = fusion.Configuration()
    if getenv('HOST_ENDPOINT'):
        configuration.host = getenv('HOST_ENDPOINT')
    if getenv('TOKEN_ENDPOINT'):
        configuration.token_endpoint = getenv('TOKEN_ENDPOINT')
    configuration.issuer_id = getenv('API_CLIENT')
    configuration.private_key_file = getenv('PRIV_KEY_FILE')

    # create an API client with your access Configuration
    base_client = fusion.ApiClient(configuration)

    # create an API client for Storage Services
    ss_client = fusion.StorageServicesApi(base_client)

    try:
        api_response = ss_client.list_storage_services()
        pprint(api_response)
    except ApiException as e:
        print("Exception when listing storage services: %s\n" % e)

if __name__ == '__main__':
    smoke_test()
