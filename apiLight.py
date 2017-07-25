#!/usr/bin/python
#
#
import RPi.GPIO as GPIO
import requests
import json

#Disable SSL cert warnings
requests.packages.urllib3.disable_warnings()

#Prepare GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

#Icinga Services API Endpoint URL
url = 'https://icinga.erad.com:5665/v1/objects/services'

#Services Group to check for
group = "crit"

#Request Headers
headers = {
    'Accept': 'application/json',
    'X-HTTP-Method-Override': 'GET'
}

#Request Data
data = {
    "joins": [ "host.name", "host.address", "host.acknowledgement", "host.downtime_depth" ],
    "attrs": [ "name", "state", "downtime_depth", "acknowledgement", "groups" ],
    "filter": "service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0 && host.acknowledgement == 0.0 && host.downtime_depth == 0.0 && \"" + group + "\" in service.groups"
}

#Initiate Request
r = requests.post(url,
    headers=headers,
    auth=('root', 'cf738ace3e5e7c8a'),
    data=json.dumps(data),
    verify=False)

#Put response in dict so we can count results easily
item_dict = json.loads(json.dumps(r.json()))

#Count results and turn on/off light accordingly
if (len(item_dict['results']) > 0):
    GPIO.output(18,True)
else: 
    GPIO.output(18,False)



if (r.status_code == 200):
    print "Result: " +  json.dumps(r.json())
else:
    print r.text
    r.raise_for_status()
