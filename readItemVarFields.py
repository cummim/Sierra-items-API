#!/usr/bin/python
#   File name:      readItemVarFields.py
#   Author:         Michael Cummings, Assistant Museum Librarian,
#                   Systems and Information Technology
#                   Thomas J. Watson Library
#                   The Metropolitan Museum of Art
#   Requirements:   Requires Sierra host, api key, and api secret loaded from
#                   a local configuration file.
#   Description:    This is a demo script. It retrieves item variable fields
#                   from Sierra and parses the results
#   Usage e.g.,:    $python readItemVarFields.py
#   
#   Set up:         Create a configuration file, local_config.cfg
#                   include lines like this in the config file
#
#[sierra]
#SIERRA_API_HOST = https://YOUR-HOST-URL
#SIERRA_API_KEY = YOUR-API=KEY
#SIERRA_API_KEY_SECRET = YOUR-API-SECRET
#
#                   point parser.read at the config file

import json
import requests
import base64
import sys
from requests import Request, Session
from datetime import date

#--------------------------------------------
# Function to pull id off hyperlink
#--------------------------------------------
def pluckId( str ):
    # Split the hyperlink string using the delimiter '/'
    parts = str.split('/')
    id_part = parts[7]
    str = id_part.replace('"}','')
    return(str);

#--------------------------------------------
# Read config file
# or replace the HOST, KEY, AND SECRET
#--------------------------------------------

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read('/home/helper/local_config.cfg')

SIERRA_API_HOST = parser.get('sierra', 'SIERRA_API_HOST')
SIERRA_API_KEY = parser.get('sierra', 'SIERRA_API_KEY')
SIERRA_API_KEY_SECRET = parser.get('sierra', 'SIERRA_API_KEY_SECRET')

AUTH_URI = '/iii/sierra-api/v5/token'
VALIDATE_URI = '/iii/sierra-api/v5/items/validate'
ITEMS_URI = '/iii/sierra-api/v5/items/'
#-----------------------------------------------
# Prepare URL, custom headers, and body for auth
#-----------------------------------------------

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
items_url = SIERRA_API_HOST + ITEMS_URI

#----------------------------------------------------------------------------
# Normally you would read the JSON file containing YOUR Sierra item links ...
# in the following code, it assumes the file name was a command line argument.
#----------------------------------------------------------------------------
#with open(sys.argv[1]) as f:
#    link_file_contents = json.load(f)
# for hyperlink in link_file_contents['entries']:

# -----------------------------------------------------
# Instead here is hardcoded link for an item at The Met
# -----------------------------------------------------

sampleitem = {
 "link": "https://www.metropolitanmuseum.org/iii/sierra-api/v5/items/1050895"
}

#-------------------------------------------------------------------------
# Reduce hyperlink to the itemid alone. Use a regex or my function pluckId
#-------------------------------------------------------------------------
itemid = pluckId(sampleitem['link'])

#-------------------------------------------------------------------
# Pass the itemid to the API call to get a barcode
# Refer to https://sandbox.iii.com/iii/sierra-api/swagger/index.html
#-------------------------------------------------------------------

payload = {'id': itemid, 'fields': 'barcode,varFields'}
items_response = requests.get(items_url, headers = request_headers, params = payload)

#--------------------------------------------------
# output response to the screen
#--------------------------------------------------

responseStr = (json.dumps(items_response.json(), indent =2))
print ("=====================================")
print ("      HERE IS THE API RESPONSE       ")
print ("=====================================")
print responseStr
print ("=====================================")

#--------------------------------------------------
# Convert the API's JSON response to Python
#--------------------------------------------------
responseData= json.loads(responseStr)
#
# ---------------------------------------------
# THIS IS HOW THE RESPONSE LOOKS
# ---------------------------------------------
# {
#  "total": 1,
#  "entries": [
#     {
#        "varFields": [
#        {
#            "content": "30620000100734",
#            "fieldTag": "b"
#        },
#        {
#            "content": "BX4363.I8|bW66 1996",
#            "fieldTag": "c"
#        },
#        {
#            "content": "9491.  7/15/98.  Cloisters Bookstore.  $75.00.  LJB.",
#            "fieldTag": "x"
#        }
#        ],
#        "barcode": "30620000100734",
#        "id": "1050895"
#      }
#   ]
# }

# ------------------------------------------------------------------
# Drill down in JSON object to get barcode, and tag c content
# ------------------------------------------------------------------
foundCallNo = False

for itemRecord in responseData['entries']:
        for tag in itemRecord['varFields']:
            if tag['fieldTag'] == "c":
                print ("Item with barcode "+itemRecord['barcode']+ \
                " has variable field tag c value of "+tag['content'])
                foundCallNo = True

if foundCallNo == False:
    # didn't find any fieldTags for "c"
    print "No call no fieldTag c was found."

print("Done ")

# -------------------------------------
# This is what it printed
# -------------------------------------
# Item with barcode 30620000100734 has variable field tag c value of BX4363.I8|bW66 1996

