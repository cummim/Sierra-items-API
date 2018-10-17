#!/usr/bin/python
#
#   file:   readItemInfo.py
#   type:   v5/items
#   date:   August 2018
#   auth:   Michael Cummings, Assistant Museum Librarian, Systems and
#           Information Technology, Thomas J. Watson Library
#   level:  stub / demo
#   desc:   Retrieve some info about a specific item.
#   usage:  This file demonstrates passing an item id as a command line
#           argument, e.g., 9999999
#           $python readItemInfo.py 9999999
#   gotcha: In this script you pass in the id from the command line
#   notes:  The script imports the sys library.
#           An item id is not the barcode or .i value; Find item ids by
#           running pgadmin query select * from sierra_view.item_view
#           This script has a try / except clause to test for the argument.
#   result: Fields from the item record; see API doc for available fields
#
# Total results: 1
#   {
#   "total": 1,
#       "entries": [
#               {
#               "barcode": "30620011278230",
#               "id": "2280904"
#               }
#         ]
#    }
#  etc... see end of this script for a more complete example.

import sys
import json
import requests
import base64
from requests import Request, Session

# -------------------------------
# Set Up Info for Sierra API 
# -------------------------------
SIERRA_API_HOST = 'https://YOURHOSTNAME'    # Hostname for Sierra API
SIERRA_API_KEY = 'YOUR API KEY'             # API key for host
SIERRA_API_KEY_SECRET = 'YOUR API SECRET'   # API secret for host

AUTH_URI = '/iii/sierra-api/v5/token'
ITEMS_URI = '/iii/sierra-api/v5/items'

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

# --------------------------------------------------------------------------------------
# the Sierra item id is passed to this script as a command line parameter 
# --------------------------------------------------------------------------------------
try:
    sys.argv[1]
    payload = {
        'id': sys.argv[1],
        'fields':
        'barcode,location,status,callNumber,itemType,createdDate,bibIds,fixedFields,varFields'
        }
    items_response = requests.get(items_url, headers = request_headers, params = payload)

    try:
        print "Total results: " + str(items_response.json()['total'])
    except KeyError:
        print "None found"
    print (json.dumps(items_response.json(), indent =4))
except IndexError:
    print " "
    print "No call was attempted."
    print "You have to provide the item id to search. Enter it on the command line"
# 
# ----------------------------------------------------------
# Results will be something like the information below. This program doesn't parse the results.
# See other examples for demos of loading results into Python and parsing the data.
# ---------------------------------------------------------
#Total results: 1
#{
#    "total": 1,
#    "entries": [
#        {
#            "status": {
#                "code": "-  ",
#                "display": "REQUESTABLE"
#            },
#            "varFields": [
#                {
#                    "content": "30620009948240",
#                    "fieldTag": "b"
#                },
#                {
#                    "content": "Shelf ready",
#                    "fieldTag": "x"
#                },
#                {
#                    "content": "on clancy offsite list 2017-11-27 lindaj",
#                    "fieldTag": "x"
#                }
#            ],
#            "itemType": "Monograph / Circ",
#            "fixedFields": {
#                "127": {
#                    "value": "0",
#                    "label": "AGENCY"
#                },
#                "60": {
#                    "value": "-",
#                    "label": "Book Conservation"
#                },
#                "61": {
#                    "display": "Monograph / Circ",
#                    "value": "0",
#                    "label": "I TYPE"
#                },
#                "88": {
#                    "display": "REQUESTABLE",
#                    "value": "-  ",
#                    "label": "STAT"
#                },
#                "64": {
#                    "value": "0",
#                    "label": "OUT LOC"
#                },
#                "110": {
#                    "value": "0",
#                    "label": "LYRCIRC"
#                },
#                "83": {
#                    "value": "2017-10-27T15:02:28Z",
#                    "label": "CREATED"
#                },
#                "80": {
#                    "value": "i",
#                    "label": "REC TYPE"
#                },
#                "81": {
#                    "value": "2289204",
#                    "label": "RECORD #"
#                },
#                "86": {
#                    "value": "1",
#                    "label": "AGENCY"
#                },
#                "84": {
#                    "value": "2017-11-27T15:42:56Z",
#                    "label": "UPDATED"
#                },
#                "85": {
#                    "value": "9",
#                    "label": "REVISIONS"
#                },
#                "264": {
#                    "value": "6",
#                    "label": "Holdings Item Tag"
#                },
#                "161": {
#                    "value": "0",
#                    "label": "VI CENTRAL"
#                },
#                "162": {
#                    "value": "0",
#                    "label": "IR DIST LEARN SAME SITE"
#                },
#                "79": {
#                    "display": "Offsite",
#                    "value": "off  ",
#                    "label": "Location(s)"
#                },
#                "306": {
#                    "value": "   ",
#                    "label": "Sticky Status"
#                },
#                "77": {
#                    "value": "0",
#                    "label": "TOT RENEW"
#                },
#                "76": {
#                    "value": "0",
#                    "label": "TOT CHKOUT"
#                },
#                "108": {
#                    "value": "-",
#                    "label": "OPACMSG"
#                },
#                "74": {
#                    "value": "0",
#                    "label": "Tech Services Use"
#                },
#                "265": {
#                    "value": "false",
#                    "label": "Inherit Location"
#                },
#                "70": {
#                    "value": "0",
#                    "label": "IN LOC"
#                },
#                "93": {
#                    "value": "0",
#                    "label": "Browse Count"
#                },
#                "94": {
#                    "value": "0",
#                    "label": "Offsite"
#                },
#                "97": {
#                    "value": "-",
#                    "label": "IMESSAGE"
#                },
#                "59": {
#                    "value": "0",
#                    "label": "PIECES"
#                },
#                "58": {
#                    "value": "1",
#                    "label": "C"
#                },
#                "98": {
#                    "value": "2017-11-27T15:42:13Z",
#                    "label": "PDATE"
#                },
#                "57": {
#                    "value": "false",
#                    "label": "BIB HOLD"
#                },
#                "62": {
#                    "value": "0.000000",
#                    "label": "PRICE"
#                },
#                "109": {
#                    "value": "0",
#                    "label": "YTDCIRC"
#                }
#            },
#            "barcode": "30620009948240",
#            "bibIds": [
#                "1906124"
#            ],
#            "location": {
#                "code": "off",
#                "name": "Offsite"
#            },
#            "createdDate": "2017-10-27T15:02:28Z",
#            "id": "2289204"
#        }
#    ]
#}
#
#



