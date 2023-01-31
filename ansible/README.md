# Ansible Playbooks

## Summary
The goal of this document is to help you set up and understand the functionality and scope of the ansible playbooks here providers.


### How run a playbook£
```
ansible-playbook playbook_name.yml
```

### Enviroment Variables
In almost every playbook, there are 2 lines that required a enviroment variable

```
app_id: "{{ ansible_env.API_CLIENT}}"
key_file: "{{ ansible_env.PRIV_KEY_FILE}}"
```
In this case, the variables are: API_CLIENT and PRIV_KEY_FILE
To set them, you can temporaly enable them with:
```
export API_CLIENT='pure1:apikey:123456789'
export PRIV_KEY_FILE='/home/user/key.pem'
```
in the case of ```PRIV_KEY_FILE```, the path to the ```key.pem``` need to be aboslute.

IF you prefer to not use enviroment variables, you can change the values inside the playbook:

```
app_id: "pure1:apikey:123456789"
key_file: "/home/user/key.pem"
```

## Folder: simple
This serie of playbooks are mean to run as standalone, no need for external input, all information required to create a resource/element are inside each playbook.
Some elements need a previous element exist to be linked.

## Folder: sample_production
This series of playbooks are mean to run based on the info inside the files on folder ```group_vars```.
Usually the name in the files are almost identical.
To detect without error what files is linked to specif playbook, inside the same, there will be a import with the value and path to the file.
```
   - include_vars: group_vars/consumer.yml
```

### sample_production/inventory.ini
Inside this file, you can declare your hosts that will act as initiators.
```
[Initiators_Hosts]
initiatorserver1
initiatorserver2
initiatorserver3
```
In this example we have declared 3 hosts, and for each one, inside folder ```host_vars```, in current folder folder, you will found a file ```.yml``` that match the name of the host initiator.
Inside there are a template that cover the minimal information ansible need to make the conection with that host.
```
ansible_user: username
ansible_host: 192.168.1.100
ansible_ssh_private_key_file: ~/.ssh/id_rsa
```
