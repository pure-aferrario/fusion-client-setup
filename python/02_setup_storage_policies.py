import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

config = fusion.Configuration()
config.issuer_id = os.getenv("API_CLIENT")
config.private_key_file = os.getenv("PRIV_KEY_FILE")

client = fusion.ApiClient(config)

ss = fusion.StorageServicesApi(api_client=client)
sc = fusion.StorageClassesApi(api_client=client)

flash_performance = fusion.StorageServicePost(
    name="flash_performance",
    display_name="flash_performance",
    hardware_types=["flash-array-x"]
)

flash_capacity = fusion.StorageServicePost(
    name="flash_capacity",
    display_name="flash_capacity",
    hardware_types=["flash-array-c"]
)

generic = fusion.StorageServicePost(
    name="generic",
    display_name="generic",
    hardware_types=["flash-array-c", "flash-array-x"]
)

db_high_performance = fusion.StorageClassPost(
    name="db_high_performance",
    display_name="db_high_performance",
    iops_limit=10000, # 10k iops
    bandwidth_limit=524288000, # 500 MB/s
    size_limit=100000000000000 # 100 TB
)

db_standard = fusion.StorageClassPost(
    name="db_standard",
    display_name="db_standard",
    iops_limit = 5000, # 5k iops
    bandwidth_limit = 262144000, # 250 MB/s
    size_limit=100000000000000 # 100 TB
)

db_bulk = fusion.StorageClassPost(
    name="db_bulk",
    display_name="db_bulk",
    iops_limit = 1000, # 1k iops
    bandwidth_limit = 52428800, # 50 MB/s
    size_limit=100000000000000 # 100 TB
)

try:        
    api_response = ss.create_storage_service(flash_performance)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)

    api_response = ss.create_storage_service(flash_capacity)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)

    api_response = ss.create_storage_service(generic)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)

    for ss_name in ["flash_capacity", "flash_performance", "generic"]:
        api_response = sc.create_storage_class(db_high_performance, ss_name)
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)

        api_response = sc.create_storage_class(db_standard, ss_name)
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)

        api_response = sc.create_storage_class(db_bulk, ss_name)
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)

except ApiException as e:
    print("Exception when calling StorageClassesApi->create_storage_class: %s\n" % e)
print("Done!")