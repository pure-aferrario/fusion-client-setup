import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

def teardown_infrastructure():
    print("Tearing down infrastructure")
    # Setup Config
    config = fusion.Configuration()
    if os.getenv('HOST_ENDPOINT'):
        config.host = os.getenv('HOST_ENDPOINT')
    if os.getenv('TOKEN_ENDPOINT'):
        config.token_endpoint = os.getenv('TOKEN_ENDPOINT')
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)
    r = fusion.RegionsApi(api_client=client)
    az = fusion.AvailabilityZonesApi(api_client=client)
    se = fusion.StorageEndpointsApi(api_client=client)
    a = fusion.ArraysApi(api_client=client)
    nig = fusion.NetworkInterfaceGroupsApi(api_client=client)

    # Get Regions
    try:
        r_list = r.list_regions()
        # pprint(r_list)
    except ApiException as e:
        print("Exception when calling RegionsApi->list_regions: %s\n" % e)
    for region in r_list.items:
        # Get Availability Zones
        try:
            az_list = az.list_availability_zones(region.name)
            # pprint(az_list)
        except ApiException as e:
            print("Exception when calling RegionsApi->list_regions: %s\n" % e)
        for availability_zone in az_list.items:
            # Get Storage Endpoints
            try:
                se_list = se.list_storage_endpoints(region.name, availability_zone.name)
                # pprint(se_list)
            except ApiException as e:
                print("Exception when calling StorageEndpointsApi->list_storage_endpoints: %s\n" % e)
            for storage_endpoint in se_list.items:
                # Delete Storage Endpoint
                print("Deleting storage endpoint", storage_endpoint.name, "in availability zone", availability_zone.name, "in region", region.name)
                try:
                    api_response = se.delete_storage_endpoint(region.name, availability_zone.name, storage_endpoint.name)
                    # pprint(api_response)
                    wait_operation_succeeded(api_response.id, client)
                except ApiException as e:
                    print("Exception when calling StorageEndpointsApi->delete_storage_endpoints: %s\n" % e)
            # Get Arrays
            try:
                a_list = a.list_arrays(region.name, availability_zone.name)
                # pprint(a_list)
            except ApiException as e:
                print("Exception when calling RegionsApi->list_regions: %s\n" % e)
            for array in a_list.items:
                # Delete Array
                print("Deleting array", array.name, "in availability zone", availability_zone.name, "in region", region.name)
                try:
                    api_response = a.delete_array(region.name, availability_zone.name, array.name)
                    # pprint(api_response)
                    wait_operation_succeeded(api_response.id, client)
                except ApiException as e:
                    print("Exception when calling ArraysApi->delete_array: %s\n" % e)
            # Get Network Interface Groups
            try:
                nig_list = nig.list_network_interface_groups(region.name, availability_zone.name)
                # pprint(nig_list)
            except ApiException as e:
                print("Exception when calling NetworkInterfaceGroupApi->list_network_interface_groups: %s\n" % e)
            for network_interface_group in nig_list.items:
                # Delete Network Interface Group
                print("Deleting network interface group", network_interface_group.name, "in availability zone", availability_zone.name, "in region", region.name)
                try:
                    api_response = nig.delete_network_interface_group(region.name, availability_zone.name, network_interface_group.name)
                    # pprint(api_response)
                    wait_operation_succeeded(api_response.id, client)
                except ApiException as e:
                    print("Exception when calling NetworkInterfaceGroupsApi->delete_network_interface_group: %s\n" % e)
            # Delete Availability Zone
            print("Deleting availability zone", availability_zone.name, "in region", region.name)
            try:
                api_response = az.delete_availability_zone(region.name, availability_zone.name)
                # pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling AvailabilitZoneApi->delete_availability_zone: %s\n" % e)
        # Delete Region
        print("Deleting region", region.name)
        try:
            api_response = r.delete_region(region.name)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except ApiException as e:
            print("Exception when calling RegionsApi->delete_region: %s\n" % e)   
    print("Done tearing down infrastructure!")

if __name__ == '__main__':
    teardown_infrastructure()