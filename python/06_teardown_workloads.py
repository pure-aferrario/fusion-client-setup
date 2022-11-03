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
t = fusion.TenantsApi(api_client=client)
ts = fusion.TenantSpacesApi(api_client=client)
pg = fusion.PlacementGroupsApi(api_client=client)
v = fusion.VolumesApi(api_client=client)
h = fusion.HostAccessPoliciesApi(api_client=client)
ss = fusion.SnapshotsApi(api_client=client)
hap = fusion.HostAccessPoliciesApi(api_client=client)

# Get all Tenants
try:
    t_list = t.list_tenants()
    pprint(t_list)
except ApiException as e:
    print("Exception when calling TenantsApi->list_tenants: %s\n" % e)

for tenant in t_list.items:
    # Get all Tenant Spaces in the Tenant
    try:
        ts_list = ts.list_tenant_spaces(tenant.name)
        pprint(ts_list)
    except ApiException as e:
        print("Exception when calling TenantSpacesApi->list_tenant_spaces: %s\n" % e)
    for tenant_space in ts_list.items:
        # Get all Volumes in the Tenant Space
        try:
            v_list = v.list_volumes(tenant.name, tenant_space.name)
            pprint(v_list)
        except ApiException as e:
            print("Exception when calling VolumesApi->list_volumes: %s\n" % e)
        for volume in v_list.items:
            # Detach all Host Access Policies from Volume
            vol_patch = fusion.VolumePatch(host_access_policies=fusion.NullableString(""))
            try:
                api_response = v.update_volume(vol_patch, tenant.name, tenant_space.name, volume.name)
                pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling VolumesApi->patch_volume: %s\n" % e)
            # Delete Volume
            try:
                api_response = v.delete_volume(tenant.name, tenant_space.name, volume.name)
                pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling VolumesApi->delete_volume: %s\n" % e)
        # Get all Snapshots in the Tenant Space
        try:
            ss_list = ss.list_snapshots(tenant.name, tenant_space.name)
            pprint(ss_list)
        except ApiException as e:
            print("Exception when calling SnapshotsApi->list_snapshots: %s\n" % e)
        for snapshot in ss_list.items:
            # Delete Snapshot
            try:
                api_response = ss.delete_snapshot(tenant.name, tenant_space.name, snapshot.name)
                pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling SnapshotsApi->delete_snapshot: %s\n" % e)
        # Get all Placement Groups in the Tenant Space
        try:
            pg_list = pg.list_placement_groups(tenant.name, tenant_space.name)
            pprint(pg_list)
        except ApiException as e:
            print("Exception when calling PlacementGroupsApi->list_placement_groups: %s\n" % e)
        for placement_group in pg_list.items:
            # Delete Placement Group
            try:
                api_response = pg.delete_placement_group(tenant.name, tenant_space.name, placement_group.name)
                pprint(api_response)
                wait_operation_succeeded(api_response.id, client)
            except ApiException as e:
                print("Exception when calling PlacementGroupsApi->delete_placement_group: %s\n" % e)
        # Delete Tenant Space
        try:
            api_response = ts.delete_tenant_space(tenant.name, tenant_space.name)
            pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except ApiException as e:
            print("Exception when calling TenantSpaceApi->delete_tenant_space: %s\n" % e)
# Get Host Access Policies
try:
    hap_list = hap.list_host_access_policies()
    pprint(hap_list)
except ApiException as e:
    print("Exception when calling HostAccessPoliciesApi->list_host_access_policies: %s\n" % e)
for host_access_policy in hap_list.items:
    # Delete Host Access Policy
    try:
        api_response = hap.delete_host_access_policy(host_access_policy.name)
        pprint(api_response)
        wait_operation_succeeded(api_response.id, client)
    except ApiException as e:
        print("Exception when calling HostAccessPoliciesApi->delete_host_access_policy: %s\n" % e)
print("Done!")