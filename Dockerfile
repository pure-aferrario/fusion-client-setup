FROM ubuntu:jammy

# Install required tools
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-pip ansible wget git bash-completion vim

# Install Python SDK and Ansible
RUN pip3 install --upgrade pip && pip3 install purefusion cryptography==3.4.8 ansible netaddr

# Install ansible's fusion collection
RUN ansible-galaxy collection install purestorage.fusion

# Get ansible playbooks and python scripts
COPY ansible ./ansible
COPY python ./python

# This is just a hack until these changes are merged into the mainline Ansible collection
COPY patches/fusion_region.py /root/.ansible/collections/ansible_collections/purestorage/fusion/plugins/modules/
COPY patches/fusion_se.py /root/.ansible/collections/ansible_collections/purestorage/fusion/plugins/modules/

# Install hmctl
RUN wget -q -O /usr/bin/hmctl https://github.com/PureStorage-OpenConnect/hmctl/releases/latest/download/hmctl-linux-amd64
RUN chmod +x /usr/bin/hmctl

COPY addon.sh ./addon.sh
RUN cat ./addon.sh >> /root/.bashrc 
