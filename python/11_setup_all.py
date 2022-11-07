import importlib
setup_infrastructure = importlib.import_module("01_setup_infrastructure")
setup_storage_policies = importlib.import_module("02_setup_storage_policies")
setup_protection_policies = importlib.import_module("03_setup_protection_policies")
setup_tenants = importlib.import_module("04_setup_tenants")
setup_workloads = importlib.import_module("05_setup_workloads")

print("Running full Fusion environment setup")
setup_infrastructure.setup_infrastructure()
setup_storage_policies.setup_storage_policies()
setup_protection_policies.setup_protection_policies()
setup_tenants.setup_tenants()
setup_workloads.setup_workloads()
print("Done with full Fusion environment setup!")