import time
import json
import sys
from threatresponse import ThreatResponse

ctrsearch = str(sys.argv[1])
#ctrsearch = 'www.ggoogle.com'
client = ThreatResponse(
    client_id='YOUR_CLIENT_ID',  # required
    client_password='YOUR_PASSWORD',  # required
    # region='us',  # optional
    # logger='<SOME LOGGER INSTANCE>',  # optional
    # proxy='<SOME PROXY URL>',  # optional
    # environment='<SPECIFIC ENVIRONMENT>' # optional
)

###-----------Observe Returns Summary of Observables
response = client.enrich.observe.observables(
    [{'type': 'domain', 'value': ctrsearch}] 
)
#print(json.dumps(response, indent=4, sort_keys=False))
jsondata = json.dumps(response, indent=4, sort_keys=False)
with open('SecureX.json', 'w') as file:
    file.write(jsondata)

