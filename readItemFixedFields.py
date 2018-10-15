#!/usr/bin/python
#   File name:      readItemFixedFields.py
#   Author:         Michael Cummings, Assistant Museum Librarian,
#                   Systems and Information Technology
#                   Thomas J. Watson Library, The Metropolitan Museum of Art

#   Requirements:   Requires Sierra host, api key, and api secret loaded from
#                   a local configuration file.
#   Description:    This is a demo script. It retrieves item fixed fields
#                   from Sierra and parses the results
#   Usage e.g.,:    python readItemFixedFields.py
#

import json
import requests
import base64
import sys
from requests import Request, Session
from datetime import date

#--------------------------------------------
# function to pull id off hyperlink
#--------------------------------------------
def pluckId( str ):
    # Split the hyperlink string using the delimiter '/'
    parts = str.split('/')
    id_part = parts[7]
    str = id_part.replace('"}','')
    return(str);

#--------------------------------------------
# Read config file
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

#------------------------------------------------------------------
# normally you would read the JSON file containing Sierra item links
#------------------------------------------------------------------
#with open(sys.argv[1]) as f:
#    link_file_contents = json.load(f)
# for hyperlink in link_file_contents['entries']:

# -------------------------------------
# instead here is hardcoded link
# -------------------------------------

sampleitem = {
 "link": "https://MYINSITUTION_URL/iii/sierra-api/v5/items/1050893"
}
#-------------------------------------
# Reduce hyperlink to the itemid alone
#-------------------------------------
itemid = pluckId(sampleitem['link'])


#--------------------------------------------------
# Pass the itemid to the API call to get a barcode
#--------------------------------------------------

payload = {'id': itemid, 'fields': 'barcode,fixedFields'}
items_response = requests.get(items_url, headers = request_headers, params = payload)
#--------------------------------------------------
# Print response to screen
# This is an example.
#
#{
#  "total": 1,
#  "entries": [
#    {
#      "barcode": "30620007566317",
#      "id": "1050893",
#      "fixedFields": {
#        "127": {
#          "value": "0",
#          "label": "AGENCY"
#        },
#        "60": {
#          "value": "-",
#          "label": "Book Conservation"
#        },
#        "61": {
#          "display": "Monograph / Circ",
#          "value": "0",
#          "label": "I TYPE"
#        },
#        "88": {
#          "display": "REQUESTABLE",
#          "value": "-  ",
#          "label": "STAT"
#        },
#        "64": {
#          "value": "0",
#          "label": "OUT LOC"
#        },
#        "110": {
#          "value": "0",
#          "label": "LYRCIRC"
#        },
#        "83": {
#          "value": "1998-12-14T17:03:00Z",
#          "label": "CREATED"
#        },
#        "80": {
#          "value": "i",
#          "label": "REC TYPE"
#        },
#        "81": {
#          "value": "1050893",
#          "label": "RECORD #"
#        },
#        "86": {
#          "value": "1",
#          "label": "AGENCY"
#        },
#        "84": {
#          "value": "2018-10-11T20:17:32Z",
#          "label": "UPDATED"
#        },
#        "85": {
#          "value": "14",
#          "label": "REVISIONS"
#        },
#        "264": {
#          "value": "6",
#          "label": "Holdings Item Tag"
#        },
#        "161": {
#          "value": "0",
#          "label": "VI CENTRAL"
#        },
#        "162": {
#          "value": "0",
#          "label": "IR DIST LEARN SAME SITE"
#        },
#        "79": {
#          "display": "Offsite",
#          "value": "off  ",
#          "label": "Location(s)"
#        },
#        "306": {
#          "value": "   ",
#          "label": "Sticky Status"
#        },
#        "77": {
#          "value": "0",
#          "label": "TOT RENEW"
#        },
#        "76": {
#          "value": "5",
#          "label": "TOT CHKOUT"
#        },
#        "108": {
#          "value": "-",
#          "label": "OPACMSG"
#        },
#        "74": {
#          "value": "0",
#          "label": "Tech Services Use"
#        },
#        "265": {
#          "value": "false",
#          "label": "Inherit Location"
#        },
#        "70": {
#          "value": "0",
#          "label": "IN LOC"
#        },
#        "93": {
#          "value": "0",
#          "label": "Browse Count"
#        },
#        "94": {
#          "value": "0",
#          "label": "Offsite"
#        },
#        "97": {
#          "value": "-",
#          "label": "IMESSAGE"
#        },
#        "59": {
#          "value": "0",
#          "label": "PIECES"
#        },
#        "58": {
#          "value": "1",
#          "label": "C"
#        },
#        "98": {
#          "value": "2016-01-27T01:16:13Z",
#          "label": "PDATE"
#        },
#        "57": {
#          "value": "false",
#          "label": "BIB HOLD"
#        },
#        "62": {
#          "value": "0.000000",
#          "label": "PRICE"
#        },
#        "109": {
#          "value": "0",
#          "label": "YTDCIRC"
#        }
#      }
#    }
#  ]
#}
# ---------------------------------------------------------

# ----------------
# OUTPUT TO SCREEN
# ----------------

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
# ------------------------------------------------------------------
# Drill down in JSON object to get barcode, create date, & total circ
# ------------------------------------------------------------------
print("Item barcode +itemRecord['barcode']+" \
" created +itemRecord['fixedFields']['83']['value']+" \
" has circulated +itemRecord['fixedFields']['76']['value']+" \
" times.")
for itemRecord in responseData['entries']:
        print("Item barcode "+itemRecord['barcode']+ \
        " created "+itemRecord['fixedFields']['83']['value']+ \
        " has circulated "+itemRecord['fixedFields']['76']['value']+ \
        " times.")

print("Done ")
# --------------------------------
# This is what prints
# --------------------------------
#Item barcode +itemRecord['barcode']+ created +itemRecord['fixedFields']['83']['value']+ has circulated +itemRecord['fixedFields']['76']['value']+ times.
#Item barcode 30620007566317 created 1998-12-14T17:03:00Z has circulated 5 times.

