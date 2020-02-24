import requests
import sys

from testscripts.const import MSB_IP

id = sys.argv[1]

requests.packages.urllib3.disable_warnings()
resp = requests.delete(MSB_IP + '/api/nsd/v1/ns_descriptors/' + id, verify=False)
print(resp.status_code)
