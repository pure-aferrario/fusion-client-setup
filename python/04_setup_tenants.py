import fusion
import os
from pprint import pprint
from utils import wait_operation_succeeded

# Setup Config
config = fusion.Configuration()
config.issuer_id = os.getenv("API_CLIENT")
config.private_key_file = os.getenv("PRIV_KEY_FILE")

client = fusion.ApiClient(config)
t = fusion.TenantsApi(api_client=client)

engineering = fusion.TenantPost(name='engineering', display_name='engineering')
finance = fusion.TenantPost(name='finance', display_name='finance')
oracle_dbas = fusion.TenantPost(name='oracle_dbas', display_name='oracle_dbas')

# Create Tenants
try:
    api_response = t.create_tenant(engineering)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)

    api_response = t.create_tenant(finance)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)

    api_response = t.create_tenant(oracle_dbas)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except Exception as e:
    print("Exception when calling ProtectionPoliciesAPI->create_tenant: %s\n" % e)
print("Done!")