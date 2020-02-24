import requests
import sys

from testscripts.const import MSB_IP, VNF_CSAR_PATH

id = sys.argv[1]

requests.packages.urllib3.disable_warnings()
url = MSB_IP + '/api/vnfpkgm/v1/vnf_packages/' + id + '/package_content'
resp = requests.put(url, files={'file': open(VNF_CSAR_PATH, 'rb')}, verify=False)
print(resp.status_code)
