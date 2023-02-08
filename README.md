
# Setting up your Fusion Demo Lab
## Summary
The goal of this document is to help you set up a machine that can connect to your Fusion environment.

If you need a high level overview of Pure Fusion please check out [this Youtube playlist](https://youtube.com/playlist?list=PLZcmbL4tTCUwv8UdACFAQZbkTtEjzob5I).
## Prerequisites
 - Pure Fusion control plane
 - Pure1 Edge Services enabled in Pure1
 - 1+ Arrays configured with Fusion Agents installed
 - An API Client (Application) registered with Pure1 and its associated private key. This API key will need Pure1 Admin permissions. The private key file must be named `private-key.pem`.

    - [API Client Creation Guide](https://support.purestorage.com/Pure_Fusion/Getting_Started_with_Pure_Fusion/Creating_and_API_Client%2F%2FApplication_Access_for_Fusion_or_Pure1_API_access)

 - Tested operating systems for the control server (testing and scripting for this project done in a Ubuntu 20.04 VM)
 *Pull requests welcomed for tested OS's and Windows Direct support*
	 - An x86-64 Ubuntu linux machine
	    - Windows WSL2 Ubuntu 20.04 or Preview
	    - (If using Docker image) Docker Desktop installed (and enabled for WSL2) 
	- An Apple M1 (arm64) or Intel (amd64) machine
	    - (If using Docker image) Docker Desktop installed
	    - wget installed 

## Setting up the Tools
The objective of this guide is to help you setup the tools you can use to interact with your Fusion environment.

There are 2 main ways to get access to the tools:
 - Downloading and using the pre-packaged Docker image
 - Running the installer to install the tools natively

**Using pre-packaged Docker image**

 - Notes: 
	 - Install Docker Desktop before proceeding for WSL2 and MacOS. If using WSL2 in Windows, ensure Docker Desktop is enabled for your distribution in the Docker settings
	 - If running on MacOS with Darwin, install `wget` before proceeding (ie. `brew install wget`)
	 - Replace API_CLIENT_ID with the APP ID from Pure1.
	 - Replace PATH_TO_PRIV_KEY with absolute path to the private-key.pem file
```
wget https://github.com/pure-aferrario/fusion-client-setup/releases/latest/download/fusion-devkit.tar
docker load < fusion-devkit.tar
mkdir api-client
echo API_CLIENT_ID > api-client/issuer
cp PATH_TO_PRIV_KEY api-client/
docker run -it -v `pwd`/api-client:/api-client fusion-devkit bash
** If running on an Apple M1 arm64 OS, use:
docker run --platform linux/amd64 -it -v `pwd`/api-client:/api-client fusion-devkit bash
```

### Using the installer bash script
```
git clone https://github.com/pure-aferrario/fusion-client-setup.git
cd fusion-client-setup
sudo chmod +x setup.sh
./setup.sh API_CLIENT_ID PATH_TO_PRIV_KEY
```

## Tools available
Here are the tools provided in this devkit:

### HMCTL
HMCTL is the remote CLI utility provided with Fusion.

To check if HMCTL was configured correctly, run
```
hmctl version
```
After this install you should be able to run commands as seen in [this guide](https://support.purestorage.com/Pure_Fusion/Pure_Fusion_for_Storage_Consumers/Example_CLI_Commands).

### Python
Our Python library has full support for all Fusion APIs.

To run the smoke test --currently broken--
```
python3 python/00_smoke_test.py
```
After installation is complete you can refer to [the documentation](https://github.com/PureStorage-OpenConnect/fusion-python-sdk) for guidance on writing your own Python scripts.

### Ansible
Our Ansible collection has full support for all Fusion APIs.

To run the smoke test --currently broken--
```
ansible-playbook smoke_test.yml
```
After installation you can check out the ansible collection from the [Ansible documentation page here](https://docs.ansible.com/ansible/latest/collections/purestorage/fusion/index.html#plugins-in-purestorage-fusion) for more information on the individual modules.

### Terraform
Our Terraform provider supports consumer workflows in Fusion. Terraform won't do a full smoke test because it is a consumer-focused provider and requires more Fusion configuration before it can execute.

After installation you can see the [Terraform module documentation here](https://registry.terraform.io/providers/PureStorage-OpenConnect/fusion/1.0.0) for guidance on writing your own Terraform templates.
