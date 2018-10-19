#!/usr/bin/python
#
#   file:   sgetitembybarcode.py
#   type:   v5/items/query
#   date:   September 2018
#   auth:   Michael Cummings, Assistant Museum Librarian, Systems and
#           Information Technology, Thomas J. Watson Library
#   level:  stub / demo
#   desc:   Run a query statement which retrieves offsite holds
#   usage:  Edit the date in the query
#           $python findItembyBarcode.py
#   gotcha: ITEMS_URI includes parameters!
#   notes:  A production version of this script is working (projects/clancy/getOffsiteholds.py)
#   result: A JSON list of link entries providing the id number of items requested from offsite
#
#          {
#          "start": 0,
#          "total": 19,
#          "entries": [
#                    {
#                     "link":
#                         "https://MYSIERRAHOST/iii/sierra-api/v5/items/1315533"
#                    },
#           etcetera

import json
import requests
import base64
from requests import Request, Session

SIERRA_API_HOST = 'https://SIERRA HOST URL'       # Hostname for Met Sierra
SIERRA_API_KEY = 'SIERRA API KEY'         # API key for host Met
SIERRA_API_KEY_SECRET = 'SIERRA API SECRET'                 # API secret for host

# Set URIs for Sierra API endpoints
AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/items/validate'

# -------------------------------------------------------------------------
# NOTE: Items URI must include query?offset=N&limit=N where N is a value
# -------------------------------------------------------------------------
ITEMS_URI = '/iii/sierra-api/v5/items/query?offset=0&limit=100'

# Create URL for auth endpoint
auth_url = SIERRA_API_HOST + AUTH_URI

# Base64 encode the API key and secret separated by a ':' (colon)
encoded_key = base64.b64encode(SIERRA_API_KEY + ':' + SIERRA_API_KEY_SECRET)

auth_headers = {'Accept': 'application/json', 'Authorization': 'Basic ' + encoded_key,'Content-Type': 'application/x-www-form-urlencoded'}

# Set grant type request for HTTP body
grant_type = 'client_credentials'  # Request a client credentials grant authorization

# Make the call to the Auth endpoint to get a bearer token
auth_response = requests.post(auth_url, headers = auth_headers, data = grant_type)
access_token = auth_response.json()['access_token']

# Create headers for making subsequent calls to the API
request_headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + access_token,'Content-Type': 'application/json'}

# Create URL for items endpoint
# ITEMS_URI = '/iii/sierra-api/v5/items/query?offset=0&limit=100'
items_url = SIERRA_API_HOST + ITEMS_URI

# Create barcode query in JSON format. An easy way to do that is to use Sierra Create Lists to create a query,
# then select JSON, then copy the JSON code, paste the JSON query into you script. Assign the name, eg., payload
# In this example, barcode assumed to be on item. Of course you could wrap this in a for loop to read a list of barcodes.
# The response will be the system id for the associted item.
# Given that item id, you can then retrieve information about the item. Here is a hard-coded example.

BARCODE = "30620009203075"
payload = {
  "queries": [
  {
    "target": {
        "record": {
        "type": "item"
         },
        "field": {
           "tag": "b"
           }
        },
        "expr": {
         "op": "equals",
         "operands": [
          BARCODE,
          ""
         ]
       }
     }
  ]
}
items_response = requests.post(items_url, headers=request_headers, json=payload)


print "RESPONSE CODE: ", items_response.status_code 
print ' '
print "Total results: " + str(items_response.json()['total'])
print "RESPONSE BODY : ", items_response.text 
print (json.dumps(items_response.json(), indent =4))

# --------------------------
# This is printed on screen:
----------------------------
# RESPONSE CODE:  200
#
# Total results: 1
# RESPONSE BODY :  {"total":1,"start":0,"entries":[{"link":"https://MYSIERRAHOST/iii/sierra-api/v5/items/2161197"}]}
# {
#     "start": 0,
#     "total": 1,
#     "entries": [
#         {
#             "link": "https://MYSIERRAHOST/iii/sierra-api/v5/items/2161197"
#         }
#     ]
# }











