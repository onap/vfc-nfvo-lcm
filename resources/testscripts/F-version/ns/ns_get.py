import requests

requests.packages.urllib3.disable_warnings()
resp = requests.get('https://192.168.235.89:30283/api/nsd/v1/ns_descriptors', verify=False)
print(resp.status_code, resp.json())
