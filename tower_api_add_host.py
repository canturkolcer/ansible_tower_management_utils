#!/usr/bin/python
import argparse
import requests
import json
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
addhost_job_name="alz_automation_utils_all_addhost2inv_template"
setChangePwd_job_name="alz_automation_utils_all_changePassword_template"
status="" #to keep status of job run

parser=argparse.ArgumentParser(description='Script used for Ansible Tower inventory management')
parser.add_argument("token", help="Token Token to run script")
parser.add_argument("fqdn", help="fqdn")
parser.add_argument("ostype", help="One of following values: linux|aix|windows")
parser.add_argument("customer_fqdn", help="Customer FQDN: hostname.domain")
parser.add_argument("adm_ip", help="ADM IP: 10.0.0.1")
parser.add_argument("ep_ip", help="EP IP: 10.1.0.1")
parser.add_argument("application", help="Application running on the server: oracle|db2|apache|none")
# parser.add_argument("vault", help="Password vault: cyberark|hashicorp")

args=parser.parse_args()

responsible_teams = '' if args.application == "none" else args.application

print("Hostname:  "+args.fqdn)
print("OS type:  " +args.ostype)
print("ADM IP:   "+args.adm_ip)
print("EP IP:    "+args.ep_ip)
print("APP:      "+args.application)
#print("Vault:    "+args.vault)
print("responsible_teams:      "+responsible_teams)

base_url="https://ansible-tower-web-svc-tower.apps.openshift.domain/api/v2/"
headers={ 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ args.token }

method="job_templates/"+addhost_job_name+"/launch/"

payload = {
 "extra_vars": {
   'name': args.fqdn,
   'tier': 'production',
   'ostype': args.ostype,
   'fqdn': args.fqdn,
   'alz_fqdn': args.customer_fqdn,
   'devicetype': 'compute',
   'ansible_host': args.adm_ip,
   'ipaddress': args.ep_ip,
   'cred_provider': 'hashicorp',
   'responsible_teams': responsible_teams
 }
}

url=base_url+method
response=requests.post(url,headers=headers,json=payload,verify=False)
r=response.json()
#print (r)

if (response.status_code == 201):
 print("Starting host adding job - Success!!!")
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
  
 print("Host adding job executed, status="+status)
else:
 print("Starting host adding job - Failure!!!")
 exit(-1)
 
if ( status == "successful"):
  method="job_templates/"+setChangePwd_job_name+"/launch/"
  
  payload = {
    "limit": "localhost, " + args.hostname_alz
  }
  
  url=base_url+method
  response=requests.post(url,headers=headers,json=payload,verify=False)
  r=response.json()
  
  if (response.status_code == 201):
    print("Starting password change job - Success!!!")
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
        
    print("Password change job executed, status="+status)
  else:
    print("Starting  password change job - Failure!!!")
    exit(-1)
  
  
