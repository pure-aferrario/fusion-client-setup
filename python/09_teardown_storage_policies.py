import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

def teardown_storage_policies():
    print("Tearing down storage policies")
    # Setup Config
    config = fusion.Configuration()
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)

    ss = fusion.StorageServicesApi(api_client=client)
    sc = fusion.StorageClassesApi(api_client=client)

    # Get all Storage Services in the environment
    try:
        ss_list = ss.list_storage_services()
        # pprint(ss_list)
    except ApiException as e:
        print("Exception when calling StorageServicesApi->list_storage_services: %s\n" % e)

    for storage_service in ss_list.items:
        # Get all Storage Classes belonging to this Storage Service
        try:
            sc_list = sc.list_storage_classes(storage_service.name)
            # pprint(sc_list)
        except ApiException as e:
            print("Exception when calling StorageServicesApi->list_storage_classes: %s\n" % e)
        for storage_class in sc_list.items:
            # Delete the Storage Class
            print("Deleting storage class", storage_class.name, "in storage service", storage_service.name)
            try:
                api_response = sc.delete_storage_class(storage_service.name, storage_class.name)
                # pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling StorageClassesApi->delete_storage_class: %s\n" % e)
        # Delete the Storage Service
        print("Deleting storage service", storage_service.name)
        try:
            api_response = ss.delete_storage_service(storage_service.name)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except ApiException as e:
            print("Exception when calling StorageServicesApi->delete_storage_service: %s\n" % e)
    print("Done tearing down storage policies!")

if __name__ == '__main__':
    teardown_storage_policies()