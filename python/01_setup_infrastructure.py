import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

# Setup Config
config = fusion.Configuration()
config.issuer_id = os.getenv("API_CLIENT")
config.private_key_file = os.getenv("PRIV_KEY_FILE")

client = fusion.ApiClient(config)
r = fusion.RegionsApi(api_client=client)
az = fusion.AvailabilityZonesApi(api_client=client)
se = fusion.StorageEndpointsApi(api_client=client)
a = fusion.ArraysApi(api_client=client)
nig = fusion.NetworkInterfaceGroupsApi(api_client=client)
ni = fusion.NetworkInterfacesApi(api_client=client)

region = "region1"
availability_zone = "az1"

network_mtu = 1500
network_interface_group = {
    "name": "interface_group1",
    "display_name": "interface_group1",
    "group_type": "eth",
    "eth": {
        "prefix": "172.17.1.0/24",
        "mtu": network_mtu
    }
}
storage_endpoint = {
    "name": "default",
    "display_name": "default",
    "endpoint_type": "iscsi",
    "iscsi": [
        {
            "address": "172.17.1.1/24",
            # "mtu": network_mtu,
            "network_interface_groups": [network_interface_group["name"]]
        },
        {
            "address": "172.17.1.2/24",
            # "mtu": network_mtu,
            "network_interface_groups": [network_interface_group["name"]]
        },
        {
            "address": "172.17.1.3/24",
            # "mtu": network_mtu,
            "network_interface_groups": [network_interface_group["name"]]
        },
        {
            "address": "172.17.1.4/24",
            # "mtu": network_mtu,
            "network_interface_groups": [network_interface_group["name"]]
        }
        ]
    }

arrays = [
    {
        "name": "flasharray1",
        "display_name": "flasharray1",
        "appliance_id": "1187351-242133817-5976825671211737520",
        "host_name": "flasharray1",
        "hardware_type": "flash-array-x"
    },
    {
        "name": "flasharray2",
        "display_name": "flasharray2",
        "appliance_id": "4044399-202674005-8936155360115641845",
        "host_name": "flasharray2",
        "hardware_type": "flash-array-x"
    }
]
# Create Region
region1 = fusion.RegionPost(name=region, display_name=region)
try:
    api_response = r.create_region(region1)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling RegionsApi->create_region: %s\n" % e)
# Create Availability Zone
az1 = fusion.AvailabilityZonePost(name=availability_zone, display_name=availability_zone)
try:
    api_response = az.create_availability_zone(az1, region1.name)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling AvailabilityZonesApi->create_availability_zone: %s\n" % e)
# Create Network Interface Group
interface_group1 = fusion.NetworkInterfaceGroupPost(
    name=network_interface_group["name"],
    display_name=network_interface_group["display_name"],
    group_type=network_interface_group["group_type"],
    eth=fusion.NetworkInterfaceGroupEthPost(
        prefix=network_interface_group["eth"]["prefix"],
        mtu=network_interface_group["eth"]["mtu"]
    )
    )
try:
    api_response = nig.create_network_interface_group(interface_group1, region1.name, az1.name)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling NetworkInterfaceGroupApi->create_network_interface_group: %s\n" % e)
# Create Storage Endpoint
default = fusion.StorageEndpointPost(
    name=storage_endpoint["name"],
    display_name=storage_endpoint["display_name"],
    endpoint_type=storage_endpoint["endpoint_type"],
    iscsi=fusion.StorageEndpointIscsiPost(
            discovery_interfaces= [ 
                fusion.StorageEndpointIscsiDiscoveryInterface(**storage_endpoint["iscsi"][0]),
                fusion.StorageEndpointIscsiDiscoveryInterface(**storage_endpoint["iscsi"][1]),
                fusion.StorageEndpointIscsiDiscoveryInterface(**storage_endpoint["iscsi"][2]),
                fusion.StorageEndpointIscsiDiscoveryInterface(**storage_endpoint["iscsi"][3]),        
            ]
        )
    )
try:
    api_response = se.create_storage_endpoint(default, region1.name, az1.name)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling StorageEndpointsApi->create_storage_endpoint: %s\n" % e)
# Add Arrays into Availability Zone
for array in arrays:
    current_array = fusion.ArrayPost(**array)
    try:
        api_response = a.create_array(current_array, region1.name, az1.name)
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)
    except ApiException as e:
        print("Exception when calling StorageEndpointsApi->create_storage_endpoint: %s\n" % e)
    patch_array = fusion.ArrayPatch(maintenance_mode=fusion.NullableBoolean(False))
    try:
        api_response = a.update_array(patch_array, region1.name, az1.name, array["name"])
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)
    except ApiException as e:
        print("Exception when calling StorageEndpointsApi->create_storage_endpoint: %s\n" % e)
print("Done!")