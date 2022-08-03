# aNSOble

Project goal is to create an automation for NSO deployment and configuration with Ansible.

Link to pipeline: https://engci-private-gpk.cisco.com/jenkins/cs-emear/job/sandbox/job/AS-Customer/job/aNSOble/
**This project may be used internally.**

## Usage

### Running aNSOble

To work with the setup first we would need a credentials to log into tail-f and GIT and download NEDs and packages.

User credentials are stored in hashed ansible-vault. To edit the data in the vault you need the go into /aNSOble folder and paste the following:

```ansible-vault edit ./setup_data_secure.yml```

Password of the vault is by default "cisco123".

Then you need to modify the vault file and edit the tail-f and GIT credentials:

```{bash}
#Server credentials and sudo password
ansible_user: cisco
ansible_password: cisco
ansible_become_password: cisco
 
#NEDs Repo Credentials
NEDsRepoUser: <NEDsRepoUser>
NEDsRepoPass: <NEDsRepoPass>
 
#GIT User Access
GITUser: <GITUser>
GITKeyPass: <GITKeyPass>
```

The next step is editing the server addresses used by the aNSOble playbook. You only need to put a proper address under the servers in the ansible_hosts file.

```{bash}
[servers]
10.48.190.167
10.48.190.168
```

Final step is running the aNSOble playbook. To run the playbook you need to run the command:

```ansible-playbook aNSOble.yml --ask-vault-pass -vvv```

If you already have one of the stages already deployed on your setup you only need to add the "skip-tags" option:

```ansible-playbook -i ansible_hosts aNSOble.yml --skip-tags “install-NSO” --ask-vault-pass -vvv```

The content of the aNSOble.yml file is the following:

```{bash}
- hosts: ubuntu
  gather_facts: no
  connection: local
  vars_files:
    - setup_data.yml
    - setup_data_secure.yml
  roles:
    - { role: Ubuntu_vcenter_deploy, tags: [ 'install vm' ] , when: VM_INSTALL }
- hosts: ubuntu
  vars_files:
    - setup_data.yml
    - setup_data_secure.yml
  roles:
    - { role: install-linux-packages, tags: [ 'install-linux-packages' ] }
    - { role: install-NSO, tags: [ 'install-NSO' ] , when: NSOInstallType is defined }
    - { role: install-NEDs, tags: [ 'install-NEDs' ] , when: NEDs is defined }
    - { role: install-repository-packages, tags: [ 'install-repository-packages' ] , when: RepositoryURL is defined }
    - { role: setup-netsim, tags: [ 'setup-netsim' ] , when: NetsimDevices is defined }
    - { role: setup-HA, tags: [ 'setup-HA' ] , when: SetupHA }
```

## Documentation

Full documentation of aNSOble can be found on SCDP page of project: ```https://scdp.cisco.com/conf/pages/viewpage.action?pageId=78614444```

## Contacts

Nicolas Fournier <coangel@cisco.com>

## AWX ( Free licensed Ansible Tower )

The AWX Collections allow Ansible Playbooks to interact with AWX(Ansible Tower). Much like interacting with AWX via the web-based UI or the API, the modules provided by the AWX Collection are another way to create, update or delete objects as well as perform tasks such as run jobs, configure Ansible Tower and more. This article will discuss new updates regarding this collection, as well as an example playbook and details on how to run it successfully.

## Installation of AWX

1. As prerequisites, below tools are required to be installed.
  **docker
  **docker-compose
  **ansible
  **node and NPM
  **git
2. download the latest AWX zip file from Github.
 $ wget https://github.com/ansible/awx/archive/17.1.0.zip
3. unzip the file
 $ unzip 17.1.0.zip
4. locate the  awx-17.1.0 folder in your directory
 $ cd awx-17.1.0 /installer
5. Open inventory and edit below details.
  admin_user=admin
  admin_password=<Strong-Admin-password>
  secret_key=<generate it>
  project_data_dir=/opt/awx_projects
6. run the Ansible playbook file called install.yml
 $ ansible-playbook -i inventory install.yml
7. To access the dashboard, launch your browser and browse the server’s IP

**access AWX UI by http://$LOCALHOST_IP

**From UI, Engineer can manage AWX organization, users, Projects, credentials creation.

**Use below APIs to fetch data from AWX List hosts --> curl -s -k --user $user:$pass http://$host_IP/api/v2/inventories/2/hosts/ | jq '.results | .[] | .name ' list templates --> curl -s -k --user $user:$pass http://$host_IP/api/v2/job_templates/ | jq '.results | .[] | .name ' List inventories --> curl -s -k --user $user:$pass http://$host_API/api/v2/inventories/ | jq '.results | .[] | .name '

**Use below API to add data at AWX UI Add host --> curl --user $user:$pass -X POST -d @host.json -H "Content-Type: application/json" -k http://$host_IP/api/v2/inventories/2/hosts/

**Use below API to trigger a template --> curl -f -k -H 'Content-Type: application/json' -XPOST  --user admin:nsoadmin http://10.78.236.119/api/v2/job_templates/7/launch/

host.json standard format will be as below host.json --> { "name": "$host_IP", "description": "this is a test host added via API", "enabled": true, "instance_id": "", "variables": "ansible_connection: ssh\nansible_password: $user_password\nansible_ssh_user: $username\nhost_key_checking: False" }

##Contacts
Mohit Kumar Pal <mohpal@cisco.com>

