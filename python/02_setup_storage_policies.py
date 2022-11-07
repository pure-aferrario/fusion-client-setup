import fusion
import os
import pathlib
import yaml
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

def setup_storage_policies():
    print("Setting up storage policies")
    # Setup Config
    config = fusion.Configuration()
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)

    ss = fusion.StorageServicesApi(api_client=client)
    sc = fusion.StorageClassesApi(api_client=client)

    # Load configuration
    with open(pathlib.Path(__file__).parent / "config/policy.yaml") as file:
        storage_services = yaml.safe_load(file)["storage_services"]

    # Create storage services
    for storage_service in storage_services:
        print("Creating storage service", storage_service["name"])
        current_storage_service = fusion.StorageServicePost(
            name=storage_service["name"],
            display_name=storage_service["display_name"],
            hardware_types=storage_service["hardware_types"]
        )
        try:        
            api_response = ss.create_storage_service(current_storage_service)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except ApiException as e:
            print("Exception when calling StorageServicesApi->create_storage_service: %s\n" % e)
        for storage_class in storage_service["storage_classes"]:
            print("Creating storage class", storage_class["name"], "in storage service", storage_service["name"])
            current_storage_class = fusion.StorageClassPost(
                name=storage_class["name"],
                display_name=storage_class["display_name"],
                iops_limit=storage_class["iops_limit"],
                bandwidth_limit=storage_class["bandwidth_limit"],
                size_limit=storage_class["size_limit"]
            )
            try:
                api_response = sc.create_storage_class(current_storage_class, current_storage_service.name)
                # pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling StorageClassesApi->create_storage_class: %s\n" % e)
    print("Done setting up storage policies!")

if __name__ == '__main__':
    setup_storage_policies()