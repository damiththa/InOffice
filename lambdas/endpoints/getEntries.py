import json
import requests
import os

import configFile as getConfigs # Config file

# airtable
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']
TBL_ENTRIES = os.environ['TBL_ENTRIES']

def handler(event, context):

    # print ('We here')

    # Getting entries from AirTable
    url = getConfigs.airTable_baseURI + AIRTABLE_BASE_KEY + '/' + TBL_ENTRIES 
    headers = {
        'Authorization': AIRTABLE_API_KEY,
        'Content-Type' : 'application/json'
    }

    getURL = url + '?' + getConfigs.airTable_urlFilter1
    # print (getURL)

    # doing GET
    resp = requests.get(getURL, headers=headers)
    # print (resp.status_code)
    # print (resp.content)

    entries = resp.json() # making resp. python friendly
    # print (entries)

    entries_keep_dict = {}
    recIDs_to_delete_lst = []

    for i in entries.keys():
        for j in entries[i]:
            thisEntry = {
                "inputDate": j['fields']['InputDate'],
                "fx_justDate": j['fields']['fx_JustDate'],
                "recID": j['id']
            }
            # print (thisEntry)

            if thisEntry['fx_justDate'] not in entries_keep_dict:
                entries_keep_dict[thisEntry['fx_justDate']] = [thisEntry['recID']]
            else:
                recIDs_to_delete_lst.append(thisEntry['recID'])
                deleteURL = url + '/' + thisEntry['recID']
                print (deleteURL)

                # doing DELETE
                resp = requests.delete(deleteURL, headers=headers)
                print (resp.status_code)
                print (resp.content)


    print(entries_keep_dict)
    print (recIDs_to_delete_lst)
    





