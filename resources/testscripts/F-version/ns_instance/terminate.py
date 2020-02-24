import json
import httplib2
import sys

from testscripts.const import MSB_IP

id = sys.argv[1]
data = {
    "gracefulTerminationTimeout": 600,
    "terminationType": "FORCEFUL"
}
headers = {'content-type': 'application/json', 'accept': 'application/json'}
ca_certs = None
auth_type = "rest_no_auth"
http = httplib2.Http(ca_certs=ca_certs, disable_ssl_certificate_validation=(auth_type == "rest_no_auth"))
http.follow_all_redirects = True
resp, resp_content = http.request(MSB_IP + '/api/nslcm/v1/ns/' + id + '/terminate',
                                  method="POST",
                                  body=json.dumps(data),
                                  headers=headers)
print(resp['status'], resp_content)
