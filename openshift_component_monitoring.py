#!/usr/bin/python3

import argparse
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# Monitor Openshift Console
# request_url="https://console-openshift-console-test.apps.openshift.domain"
request_url="https://console-openshift-console.apps.openshift.domain"

res = requests.get(
  request_url,
  timeout=60,
  verify=False
)

if ( res.status_code == 200 ):
      print("[SUCCESS] Openshift Console is reachable. HTTP Status Code: ", res.status_code)
else:
      print("[FAILED] Openshift Console is not reachable. HTTP Status Code: ", res.status_code)
      
# Monitor NEXT URL
# request_url="https://next-test.apps.openshift.domain/tupix/tickets"
request_url="https://next.apps.openshift.domain/tupix/tickets"
# Uses readonly monitoring api user (monitoring) on NEXT.
request_header={'Content-Type': 'application/json', 'Authorization': 'Basic ******' }

res = requests.get(
    request_url,
    headers=request_header,
    timeout=60,
    verify=False
)

if ( res.status_code == 200 ):
      print("[SUCCESS] NEXT is reachable. HTTP Status Code: ", res.status_code)
else:
      print("[FAILED] NEXT is not reachable. HTTP Status Code: ", res.status_code)

# Monitor Tower
# request_url="https://1ansible-tower-web-svc-tower.apps.openshift.domain/api/v2/metrics/?format=json"
request_url="https://ansible-tower-web-svc-tower.apps.openshift.domain/api/v2/metrics/?format=json"
request_header={'Content-Type': 'application/json', 'Authorization': 'Bearer *****' }

res = requests.get(
    request_url,
    headers=request_header,
    timeout=60,
    verify=False
)

if ( res.status_code == 200 ):
      print("[SUCCESS] Ansible Tower is reachable. HTTP Status Code: ", res.status_code)
      
      if ( res.json()['awx_pending_jobs_total']['value'] >= 20 ):
        print("[FAILED] Ansible Tower has more than 20 pending jobs in queue. Pending Job Total: ", res.json()['awx_pending_jobs_total']['value'])
      else:
        print("[SUCCESS] Ansible Tower has less than 20 pending jobs in queue. Pending Job Total: ", res.json()['awx_pending_jobs_total']['value'])  
else:
      print("[FAILED] Ansible Tower is not reachable. HTTP Status Code: ", res.status_code)


# Monitor Hashicorp Vault
# request_url="https://hashicorp-int.apps.openshift.domain"
request_url="https://hashicorp.apps.openshift.domain"

res = requests.get(
  request_url,
  timeout=60,
  verify=False
)

if ( res.status_code == 200 ):
      print("[SUCCESS] Hashicorp Vault is reachable. HTTP Status Code: ", res.status_code)

      request_url="https://hashicorp.apps.openshift.domain/v1/monitoring/data/check"
      request_header={ 'X-Vault-Request': 'true', 'Content-Type': 'application/json', 'X-Vault-Token': 's.*****'}

      payload = { 
          "data": 
            { 
             "test_data": "success"
             } 
            }      
      
      res = requests.post(
        request_url,
        headers=request_header,
        json=payload,
        timeout=60,
        verify=False
      )
      
      if ( res.status_code == 200 ):
            print("[SUCCESS] Hashicorp Vault is writable. HTTP Status Code: ", res.status_code)
            
            request_url="https://hashicorp.apps.openshift.domain/v1/monitoring/metadata/check"
            res = requests.delete(
              request_url,
              headers=request_header,
              timeout=60,
              verify=False
            )
            
      else:
            print("[FAILED] Hashicorp Vault is not writable. HTTP Status Code: ", res)

else:
      print("[FAILED] Hashicorp Vault is not reachable. HTTP Status Code: ", res.status_code)

# Monitor SFS
# request_url="https://esfs-int-secure-file-service-ui.apps.openshift.domain/"
request_url="https://sfs-secure-file-service-ui.apps.openshift.domain/"

res = requests.get(
  request_url,
  timeout=60,
  verify=False
)

if ( res.status_code == 200 ):
      print("[SUCCESS] Secure File Service is reachable. HTTP Status Code: ", res.status_code)
else:
      print("[FAILED] Secure File Service is not reachable. HTTP Status Code: ", res.status_code)
   
