import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

def teardown_tenants():
    print("Tearing down tenants")
    # Setup Config
    config = fusion.Configuration()
    if os.getenv('HOST_ENDPOINT'):
        config.host = os.getenv('HOST_ENDPOINT')
    if os.getenv('TOKEN_ENDPOINT'):
        config.token_endpoint = os.getenv('TOKEN_ENDPOINT')
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)
    t = fusion.TenantsApi(api_client=client)

    engineering = fusion.TenantPost(name='engineering', display_name='engineering')
    finance = fusion.TenantPost(name='finance', display_name='finance')
    oracle_dbas = fusion.TenantPost(name='oracle_dbas', display_name='oracle_dbas')

    # Get all Tenants
    try:
        t_list = t.list_tenants()
        # pprint(t_list)
    except ApiException as e:
        print("Exception when calling TenantsApi->list_tenants: %s\n" % e)
    for tenant in t_list.items:
        # Delete Tenant
        print("Deleting tenant", tenant.name)
        try:
            api_response = t.delete_tenant(tenant.name)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except ApiException as e:
            print("Exception when calling TenantsApi->delete_tenant: %s\n" % e)
    print("Done tearing down tenants!")

if __name__ == '__main__':
    teardown_tenants()