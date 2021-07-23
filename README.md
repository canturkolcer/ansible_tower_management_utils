** Assembly Line Playbooks **

1. General Information

Assembly Line playbooks are run by a python code which uses *res2api* user with its token.
Each playbook runs with res2api token assigned in template and proceed with res2api user. Credential "ao1_cred_res2api_token" created with this reason. "res2api" user credentials are stored in hashicorp vault under path "infrastructure -> res2api".

to get those scripts, you can clone following gitlab repository:
https://fre2git021ccpr1.openshift.domain/Continuous-Engineering/ansible_collection_eventautomation_utils.git

2. Add host to Ansible Tower

tower_api_add_host.py will be used.

```
tower_api_add_host.py <tower token> <IBM Hostname> <OS type - linux|aix|windows> <Allianz Hostname> <ADM IP> <EP IP> <Application running on the server: comma seperated team names list | none >

```

* Team names should be gathered from Automation team.

Server will be added to tower with os groups and the groups you will provide as application. All assignments will be made during the run and server initial password will be stored to hashicorp even if server is marked as Cyberark (GPAM) because at server build Server won't be boarded to cyberark

2. Onboard host to Cyberark

tower_api_onboard_host_cya.py will be used

```
tower_api_onboard_host_cya.py <tower token> <IBM Hostname>
```

3. Remove Host from Ansible Tower

tower_api_remove_host.py will be used.

```
./tower_api_remove_host.py <tower token> <IBM Hostname>
```
