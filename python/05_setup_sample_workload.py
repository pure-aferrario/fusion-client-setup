import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

config = fusion.Configuration()
config.issuer_id = os.getenv("API_CLIENT")
config.private_key_file = os.getenv("PRIV_KEY_FILE")

client = fusion.ApiClient(config)
ts = fusion.TenantSpacesApi(api_client=client)
pg = fusion.PlacementGroupsApi(api_client=client)
v = fusion.VolumesApi(api_client=client)
h = fusion.HostAccessPoliciesApi(api_client=client)

region = "region1"
availability_zone="az1"
tenant = 'oracle_dbas'
tenant_space = "db_tenant_space"
placement_group = "pg1"
storage_service = "flash_performance"
iqn= "iqn.2005-03.com.RedHat:linux-host1"
personality = "linux"

# Create Tenant-Space for our DB application
sample_tenant_space = fusion.TenantSpacePost(
    name=tenant_space,
    display_name=tenant_space
)

try:
    api_response = ts.create_tenant_space(sample_tenant_space, tenant)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling TenantSpacesApi->create_tenant_space: %s\n" % e)
    quit()

# Create Placement Group for our Volumes
pg1 = fusion.PlacementGroupPost(
    name=placement_group,
    display_name=placement_group,
    region=region,
    availability_zone=availability_zone,
    storage_service=storage_service
)

try:
    api_response = pg.create_placement_group(pg1, tenant, tenant_space)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling PlacementGroupApi->create_placement_group: %s\n" % e)
    quit()

# Create Volumes

data_vol1 = fusion.VolumePost(
    name="data_vol1",
    display_name="data_vol1",
    size=5000000000000, # 5TB
    storage_class="db_high_performance",
    placement_group=placement_group,
    protection_policy="db_fifteen"
)

data_vol2 = fusion.VolumePost(
    name="data_vol2",
    display_name="data_vol2",
    size=5000000000000, # 5TB
    storage_class="db_high_performance",
    placement_group=placement_group,
    protection_policy="db_fifteen"
)

log_vol = fusion.VolumePost(
    name="log_vol",
    display_name="log_vol",
    size=1000000000000, # 1TB
    storage_class="db_standard",
    placement_group=placement_group,
    protection_policy="db_fifteen"
)

config_volume = fusion.VolumePost(
    name="config_vol",
    display_name="config_vol",
    size=500000000000, # 5TB
    storage_class="db_bulk",
    placement_group=placement_group,
    protection_policy="db_fifteen"
)

try:
    api_response = v.create_volume(data_vol1, tenant, tenant_space)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.create_volume(data_vol2, tenant, tenant_space)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.create_volume(log_vol, tenant, tenant_space)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.create_volume(config_volume, tenant, tenant_space)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling VolumesApi->create_volume: %s\n" % e)
    quit()

# Create Host-Access-Policy
db_hap = fusion.HostAccessPoliciesPost(name="customer_host_access", display_name="customer_host_access", iqn=iqn, personality=personality)

try:
    api_response = h.create_host_access_policy(db_hap)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling HostAccessPolicyApi->create_host_access_policy: %s\n" % e)
    quit()

# Assign Host-Access-Policy with Volumes

data_vol1_hap_assignment = fusion.VolumePatch(host_access_policies=fusion.NullableString("customer_host_access"))
data_vol2_hap_assignment = fusion.VolumePatch(host_access_policies=fusion.NullableString("customer_host_access"))
log_volume_hap_assignment = fusion.VolumePatch(host_access_policies=fusion.NullableString("customer_host_access"))
config_volume_hap_assignment = fusion.VolumePatch(host_access_policies=fusion.NullableString("customer_host_access"))

try:
    api_response = v.update_volume(data_vol1_hap_assignment, tenant, tenant_space, "data_vol1")
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.update_volume(data_vol2_hap_assignment, tenant, tenant_space, "data_vol2")
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.update_volume(log_volume_hap_assignment, tenant, tenant_space, "log_vol")
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
    api_response = v.update_volume(config_volume_hap_assignment, tenant, tenant_space, "config_vol")
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling VolumesApi->patch_volume: %s\n" % e)
print("Done!")