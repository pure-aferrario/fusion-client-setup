# Setting up your Fusion Demo Lab
## Summary
The goal of this document is to help you set up a machine that can connect to your Fusion environment.

If you need a high level overview of Pure Fusion please check out [this Youtube playlist](https://youtube.com/playlist?list=PLZcmbL4tTCUwv8UdACFAQZbkTtEjzob5I).
## Pre-Requisites
- Pure Fusion control plane
- Pure1 Edge Services enabled in Pure1
- 1+ Arrays configured with Fusion Agents installed
- An API Client (Application) registered with Pure1 and its associated private key. This API key will need Pure1 Admin permissions.
    - [API Client Creation Guide](https://support.purestorage.com/Pure_Fusion/Getting_Started_with_Pure_Fusion/Creating_and_API_Client%2F%2FApplication_Access_for_Fusion_or_Pure1_API_access)
- An x86-64 Ubuntu linux machine as your control server
    - Windows WSL2 with Ubuntu 20.04 is tested working and is actually the author's setup
    - Testing and scripting for this project done in a Ubuntu 20.04 vm
    - Pull requests for direct Windows and MacOS support welcome
## Setting up Tools
The objective of this guide is to help you setup the tools you can use to interact with your Fusion environment. To that end, you should start by making the setup script executable and running it.
```
sudo chmod +x setup.sh
setup.sh
```
Running this script will set up the following.
### HMCTL
HMCTL is the remote CLI utility provided with Fusion. The setup.sh script will install this and configure your profile so that you will be able to interact with your Fusion environment using the API client you provide. It will also run a smoke test to make sure HMCTL is working.

After this install you should be able to run commands as seen in [this guide](https://support.purestorage.com/Pure_Fusion/Pure_Fusion_for_Storage_Consumers/Example_CLI_Commands).
### Python
Our Python library has full support for all Fusion APIs. The setup.sh script will install the needed dependencies and run a smoke test to make sure it works.

After installation is complete you can refer to [the documentation](https://github.com/PureStorage-OpenConnect/fusion-python-sdk) for guidance on writing your own Python scripts.
### Ansible
Our Ansible collection has full support for all Fusion APIs. The setup.sh script will install Ansible and needed dependencies and run a smoke test to make sure it's working.

After installation you can check out the ansible collection from the [Ansible documentation page here](https://docs.ansible.com/ansible/latest/collections/purestorage/fusion/index.html#plugins-in-purestorage-fusion) for more information on the individual modules.

### Terraform
Our Terraform provider supports consumer workflows in Fusion. The setup.sh script will install Terraform and needed dependencies and verify that it is ready. Terraform won't do a full smoke test because it is a consumer-focused provider and requires more Fusion configuration before it can execute.

After installation you can see the [Terraform module documentation here](https://registry.terraform.io/providers/PureStorage-OpenConnect/fusion/1.0.0) for guidance on writing your own Terraform templates.