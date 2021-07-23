#!/usr/bin/python
import argparse
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
offboarding_job_name="alz_automation_utils_all_removehost_template"
status="" #to keep status of job run

parser=argparse.ArgumentParser(description='Script used for Ansible Tower inventory management')
parser.add_argument("token", help="Token Token to run script")
parser.add_argument("hostname", help="hostname")

args=parser.parse_args()

print("Hostname:  "+args.hostname)

args.hostname_alz="alz_"+args.hostname

base_url="https://ansible-tower-web-svc-tower-int.apps.openshift.domain/api/v2/"
headers={ 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ args.token }

method="job_templates/"+offboarding_job_name+"/launch/"

payload = {
 "extra_vars": {
   'hostname': args.hostname
 }
}

url=base_url+method
response=requests.post(url,headers=headers,json=payload,verify=False)
r=response.json()

if (response.status_code == 201):
 print("Starting host removing job - Success!!!")
 time.sleep(2)
 method="jobs/?id="+str(r['id'])
 print(method)
 url=base_url+method
 payload= {}

 while True:
  response2=requests.get(url,headers=headers,json=payload,verify=False)
  r2=response2.json()
  status=r2['results'][0]['status']
  print(status)
  if status == "failed" or status == "successful" or status == "error" or status == "canceled":
   break
  time.sleep(2)
  
 print("Host removing job executed, status="+status)
else:
 print("Removing host adding job - Failure!!!")
 exit(-1)
   
