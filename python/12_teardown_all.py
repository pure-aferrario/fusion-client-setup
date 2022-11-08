import importlib
teardown_workloads = importlib.import_module("06_teardown_workloads")
teardown_tenants = importlib.import_module("07_teardown_tenants")
teardown_protection_policies = importlib.import_module("08_teardown_protection_policies")
teardown_storage_policies = importlib.import_module("09_teardown_storage_policies")
teardown_infrastructure = importlib.import_module("10_teardown_infrastructure")

print("Running full Fusion environment teardown")
teardown_workloads.teardown_workloads()
teardown_tenants.teardown_tenants()
teardown_protection_policies.teardown_protection_policies()
teardown_storage_policies.teardown_storage_policies()
teardown_infrastructure.teardown_infrastructure()
print("Done with full Fusion environment teardown!")