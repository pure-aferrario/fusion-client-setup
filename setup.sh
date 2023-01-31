#!/bin/bash

# Args
apiClient="$1"
pathToKey="$2"

red='\033[0;31m'
green='\033[0;32m'
blue='\033[0;34m'
nocolor='\033[0m'

echo -e "${red}"
# check this scripts is given 2 argvs
if [ "$#" -ne 2 ]; then
    echo "Missing parameters: API_CLIENT and PRIV_KEY_FILE"
    echo -e "${blue}Run: $0 API_CLIENT PRIV_KEY_FILE${nocolor}"
    exit
fi

# Check if apiClient argv is empty
if [[ -z "$apiClient" ]]; then
  echo "Missing API Client ID"
  exit
fi
# Check if pathToKey argv is empty
if [[ -z "$pathToKey" ]]; then
  echo "Missing Private Key path"
  exit
elif ! [[ -f "$pathToKey" ]]; then # check if pathToKey is not a valid file
  echo "Private Key is not a valid file: $pathToKey"
  exit
fi

# check that pathToKey is absolute and not relative
# absolute = /home/user/folder/priv_key.pem
# relative = private_key.pem
case $pathToKey in
  /*) echo -e "${green}Starting install setup${nocolor}" ;;
   *) echo -e "Please use absolute path for private key: $pathToKey${nocolor}"
      echo -e "Example: $(pwd)/$pathToKey"
      exit ;;
esac

export API_CLIENT="$apiClient"
export PRIV_KEY_FILE="$pathToKey"

echo "
██████  ██    ██ ██████  ███████ ███████ ████████  ██████  ██████   █████   ██████  ███████
██   ██ ██    ██ ██   ██ ██      ██         ██    ██    ██ ██   ██ ██   ██ ██       ██
██████  ██    ██ ██████  █████   ███████    ██    ██    ██ ██████  ███████ ██   ███ █████
██      ██    ██ ██   ██ ██           ██    ██    ██    ██ ██   ██ ██   ██ ██    ██ ██
██       ██████  ██   ██ ███████ ███████    ██     ██████  ██   ██ ██   ██  ██████  ███████
"

# detect OS name
os_name=$(cat /etc/os-release | grep "^ID=" | head -1)
if [[ "$os_name" == *"centos"* ]]; then
  os_name="Centos"
elif [[ "$os_name" == *"buntu"* ]]; then
  os_name="Ubuntu"
else
  echo -e "${red}Cant detect OS${nocolor}"
  exit
fi

# HMCTL setup

if [ $os_name == "Centos" ]; then
  sudo yum -y install wget
fi

echo -e "${blue}################################"
echo -e "#         HMCTL setup          #"
echo -e "################################${nocolor}"

echo -e "${green}Downloading HMCTL..."
if [ $os_name == "Centos" ]; then
  sudo wget -O /usr/bin/hmctl https://github.com/PureStorage-OpenConnect/hmctl/releases/latest/download/hmctl-linux-amd64
else
  sudo wget -q --show-progress -O /usr/bin/hmctl https://github.com/PureStorage-OpenConnect/hmctl/releases/latest/download/hmctl-linux-amd64
fi

# check last command exit status
if [ $? -eq 0 ]; then
  echo -e "${green}HMCTL download to: /usr/bin/hmctl"
else
  echo -e "${red}HMCTL fail to download"
  exit
fi
# give hmctl execute permissions
sudo chmod +x /usr/bin/hmctl
# create folder .pure under home folder
mkdir -p ~/.pure/
# create file: ~/.pure/fusion.json (replace if exist)
echo '{
  "default_profile": "main",
  "profiles": {
    "main": {
      "env": "pure1",
      "endpoint": "https://api.pure1.purestorage.com/fusion",
      "auth": {
        "issuer_id": "'${apiClient}'",
        "private_pem_file": "'${pathToKey}'"
      }
    }
  }
}' > ~/.pure/fusion.json

# HMCTL test
hmctl region list

# Python setup
echo -e "${blue}################################"
echo -e "#         Python setup         #"
echo -e "################################${nocolor}"

if [ $os_name == "Centos" ]; then
  sudo yum -y install python3-pip
  sudo pip3 install --upgrade pip
else
  sudo apt -qq update
  sudo apt install -y python3-pip
fi

echo -e "${blue}################################"
echo -e "#    Python Lib: Purefusion    #"
echo -e "################################${nocolor}"
pip3 install purefusion
pip3 install netaddr
pip3 install cryptography==3.4.8

# Python smoke test
echo -e "${blue}################################"
echo -e "#      Python smoke test       #"
echo -e "################################${nocolor}"
sudo chmod +x python/00_smoke_test.py
python3 python/00_smoke_test.py

# check if last command fail
if [ $? -eq 1 ]; then
  echo -e "${red}################################"
  echo -e "#   FAIL: Python smoke test    #"
  echo -e "################################${nocolor}"
fi

# Ansible setup
echo -e "${blue}################################"
echo -e "#         Ansible setup        #"
echo -e "################################${nocolor}"
pip3 install ansible
ansible-galaxy collection install purestorage.fusion
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix

# Ansible test
echo -e "${blue}################################"
echo -e "#     Ansible smoke test     #"
echo -e "################################${nocolor}"
ansible-playbook ansible/smoke_test.yml

# check if last command fail
if [ $? -eq 0 ]; then
    # if success
  echo -e "${green}################################"
  echo -e "#     OK:Ansible smoke test     #"
  echo -e "################################${nocolor}"
else
  echo -e "${red}################################"
  echo -e "#    FAIL:Ansible smoke test   #"
  echo -e "################################${nocolor}"
fi

# Terraform setup
echo -e "${blue}################################"
echo -e "#       Terraform setup        #"
echo -e "################################${nocolor}"
if [ $os_name == "Centos" ]; then
  sudo yum install -y yum-utils
  sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
  sudo yum -y install terraform
else
  # install dependencies
  sudo apt install -y gnupg software-properties-common
  # download gpg key
  wget -q -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg >/dev/null 2>&1
  # add gpg key
  gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
  # add repo file to /etc/apt/sources.list.d
  echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
      https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
      sudo tee /etc/apt/sources.list.d/hashicorp.list

  sudo apt -qq update
  sudo apt install -y terraform
fi

# Terraform test
echo -e "${blue}################################"
echo -e "#       Terraform test        #"
echo -e "################################${nocolor}"

color_terraform="$red"
terraform_version=$(terraform -version)
# check last command exit status
if [ $? -eq 0 ]; then
  color_terraform="$green"
fi
echo -e "${color_terraform}################################"
echo -e "$terraform_version"
echo -e "################################${nocolor}"
