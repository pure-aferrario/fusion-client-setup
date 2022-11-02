import fusion
import os
from fusion.rest import ApiException
from pprint import pprint
from utils import wait_operation_succeeded

config = fusion.Configuration()
config.issuer_id = os.getenv("API_CLIENT")
config.private_key_file = os.getenv("PRIV_KEY_FILE")

client = fusion.ApiClient(config)
pp = fusion.ProtectionPoliciesApi(api_client=client)

db_fifteen = fusion.ProtectionPolicyPost(name='db_fifteen', display_name='db_fifteen', objectives=[{"type": "RPO", "rpo": "PT15M"}, {"type": "Retention", "after": "PT24H"}])
hourly_for_a_week = fusion.ProtectionPolicyPost(name='hourly_for_a_week', display_name='hourly_for_a_week', objectives=[{"type": "RPO", "rpo": "PT1H"}, {"type": "Retention", "after": "PT168H"}])
daily_for_a_month = fusion.ProtectionPolicyPost(name='daily_for_a_month', display_name='daily_for_a_month', objectives=[{"type": "RPO", "rpo": "PT24H"}, {"type": "Retention", "after": "PT730H"}])

try:
    api_response = pp.create_protection_policy(db_fifteen)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except Exception as e:
    print("Exception when calling ProtectionPoliciesAPI->create_protection_policy: %s\n" % e)
    if e.pure_code != 'ALREADY_EXISTS':
        quit()

try:
    api_response = pp.create_protection_policy(hourly_for_a_week)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling ProtectionPoliciesAPI->create_protection_policy: %s\n" % e)
    if e.pure_code != 'ALREADY_EXISTS':
        quit()

try:
    api_response = pp.create_protection_policy(daily_for_a_month)
    pprint(api_response)
    wait_operation_succeeded(api_response.id, client)
except ApiException as e:
    print("Exception when calling ProtectionPoliciesAPI->create_protection_policy: %s\n" % e)
    if e.pure_code != 'ALREADY_EXISTS':
        quit()
print("Done!")