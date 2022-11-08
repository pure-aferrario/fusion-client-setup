import fusion
import os
import pathlib
import yaml
from pprint import pprint
from utils import wait_operation_succeeded

def setup_tenants():
    print("Setting up tenants")
    # Setup Config
    config = fusion.Configuration()
    config.issuer_id = os.getenv("API_CLIENT")
    config.private_key_file = os.getenv("PRIV_KEY_FILE")

    client = fusion.ApiClient(config)
    t = fusion.TenantsApi(api_client=client)

    # Load configuration
    with open(pathlib.Path(__file__).parent / "config/tenants.yaml") as file:
        tenants = yaml.safe_load(file)

    # Create Tenants
    for tenant in tenants:
        print("Creating tenant", tenant["name"])
        current_tenant = fusion.TenantPost(name=tenant["name"], display_name=tenant["display_name"])
        try:
            api_response = t.create_tenant(current_tenant)
            # pprint(api_response)
            wait_operation_succeeded(api_response.id, client)
        except Exception as e:
            print("Exception when calling TenantsAPI->create_tenant: %s\n" % e)
    print("Done setting up tenants!")

if __name__ == '__main__':
    setup_tenants()