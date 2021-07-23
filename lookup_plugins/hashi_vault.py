# -----------------------
# Owner: Canturk Olcer, 2020
# Altered from (c) 2017, Edward Nunez <edward.nunez@cyberark.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
DOCUMENTATION = """
    lookup: hashi_vault.py
    version_added: "1.1"
    short_description: get secrets from CyberArk AIM and HashiCorp Vault
    requirements:
      - Plugin to be added to repository under same directory with main playbook to be run with following directory structure :  lookup_plugins > hashi_vault.py 
    description:
      - get secrets from CyberArk AIM and HashiCorp Vault
    parameters :
      cred_provider:
        description: Defines if it is cyberark or hashicorp vault query
        required: True
      fqdn_vault:
        description: Lookup value for hashicorp vault
        required: True
      fqdn_cya:
        description: Lookup value for cyberark
        required: True        
      ostype:
        description: OS type of host to set proper query
        required: True
      datacenter:
        description: Location of server, which is needed to find out which cyberark instance to query
        required: True        
      output:
        description:
          - Specifies the desired output fields separated by commas.
          - "They could be: Password, PassProps.<property>, PasswordChangeInProcess"
        default: 'password'
"""
EXAMPLES = """

ansible_password: |-
   {{ lookup("hashi_vault", {
           "cred_provider": "{{ cred_provider }}", 
           "fqdn_vault": "{{ fqdn }}",
           "fqdn_cya": "{{ cya_fqdn }}"           
           "ostype": "{{ ostype }}",
           "datacenter": "{{ datacenter }}"  } ) }}

"""
RETURN = """
  password:
    description:
      - The actual value stored
"""
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from urllib import urlencode, quote
from urlparse import urljoin
import requests
display = Display()
class HashiCorpPassword:
    def __init__(self, datacenter=None, app_id=None, ostype=None, fqdn_vault=None, token=None, output=None, **kwargs):
        self.url = "https://hashicorp.vault/v1/automation/data/" + ostype + "/" + fqdn_vault
        self.token = "s.*****"

        self.output = output

    def get(self):

        request_url = self.url
        request_header = {'X-Vault-Token': self.token,  'X-Vault-Request': 'true', 'Content-Type': 'application/json'}
        res = requests.get(
            request_url,
            headers=request_header,
            timeout=60,
            verify=False
        )

        if res.status_code == 500:
            res = requests.get(
                request_url,
                headers=request_header,
                timeout=60,
                verify=False
            )

        if res.status_code == 404:
            return ""
        
        return res.json()['data']['data']['password']
    
class CyberarkPassword:
    def __init__(self, datacenter=None, app_id=None, ostype=None, fqdn_cya=None, object_query_format="Exact", output=None, **kwargs):
         
        cyberarkUrls = {
          "e1" : "https://url1",
          "e2" : "https://url2"
        }
        
        cyberarkQueries = {
          "windows":"Object=WIN-hostname-winuser",
          "aix":"Object=AIX-hostname-aixuser",
          "linux":"Object=LIN-hostname-linuxuser"
        }    
        
        app_id = "DynamicAutomation"
        url = cyberarkUrls[datacenter]
        query = cyberarkQueries[ostype].replace("hostname", fqdn_cya)
        
        self.url = url
        self.app_id = app_id
        self.query = query
        self.output = output
        self.object_query_format = object_query_format
        #display.vvvv("in cyberark init: %s" % self)
        
    def get(self):
        #result_dict = {}
        query_params = {
            'AppId': self.app_id,
            'Query': self.query,
            'QueryFormat': self.object_query_format,
        }
        #display.vvvv("in cyberark get: %s" % query_params)
        request_qs = '?' + urlencode(query_params)
        request_url = urljoin(self.url, '/'.join(['AIMWebService', 'api', 'Accounts']))
         
        res = requests.get(
            request_url + request_qs,
            timeout=60,
            verify=False
        )
        
        if res.status_code == 500:
            res = requests.get(
                request_url + request_qs,
                timeout=60,
                verify=False
            )
            
        if res.status_code == 404:
            return ""
          
        return res.json()['Content']
        
class LookupModule(LookupBase):
    """
    USAGE:
    """
    def run(self, terms, variables=None, **kwargs):
        display.vvvv("Display passed params: %s" % terms)
        # Display passed params: [{'ostype': u'windows', 'cred_provider': u'cyberark', 'fqdn_vault': u'sm017653.wwg00m.rootdom.net', 'fqdn_cya': u'sm017653.wwg00m.rootdom.net', 'datacenter': u'E1'}]
        provider = terms[0]['cred_provider']
        
        if isinstance(terms, list):
            return_values = []
            for term in terms:
                # display.vvvv("Term: %s" % term)
                if provider == 'hashicorp':
                  hashicorp_conn = HashiCorpPassword(**term)
                  return_values.append(hashicorp_conn.get())
                elif provider == 'cyberark':
                  cyberark_conn = CyberarkPassword(**term)
                  return_values.append(cyberark_conn.get())
            return return_values
        else:
            if provider == 'hashicorp':
              hashicorp_conn = HashiCorpPassword(**terms)
              result = hashicorp_conn.get()
              return result
            elif provider == 'cyberark':
              cyberark_conn = CyberarkPassword(**terms)
              result = cyberark_conn.get()
              return result
