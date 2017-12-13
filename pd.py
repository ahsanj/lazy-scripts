#!/usr/bin/python
'''
usage: create a file called config.py in the same directory and add your PagerDuty API key
api_key= " "  
'''
'''
***schedules***
https://xxxx.pagerduty.com/schedules#P5VS9U8 - wing
https://xxxx.pagerduty.com/schedules#PLWJB2W - tindia
'''
import requests
import json
import sys
import config

API_KEY = config.api_key

TIME_ZONE = 'UTC'
#SRE_SCHEDULE_IDS = ['P5VS9U8']
#TI_SCHEDULE_IDS =['PLWJB2W']
#SCHEDULE_IDS= TI_SCHEDULE_IDS


def oncall_sre(SCHEDULE_IDS):
    url = 'https://api.pagerduty.com/oncalls'
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=API_KEY)
    }
    payload = {
        'time_zone': TIME_ZONE,
        'schedule_ids[]': SCHEDULE_IDS,  
    }

    req = requests.get(url, headers=headers, params=payload)

    #if req.status_code not in range(200, 300):
    #    print "Request didnt go through, status returned: ",req.status_code
    #else:
    #    print "Request accepted: ",req.status_code
    data= req.json()['oncalls']
    new_data= data[0]
    print new_data['user']['summary'], "- Is oncall!"
    

def main():
    if len(sys.argv) == 1:
        print 'usage: ./pd.py {wing | tindia}'
        sys.exit(1)
    if  sys.argv[1] == "wing" or "tindia":
        option = sys.argv[1]
        if option == 'wing':
            SCHEDULE_IDS = ['P5VS9U8']
            oncall_sre(SCHEDULE_IDS)
        elif option == 'tindia':
            SCHEDULE_IDS =['PLWJB2W']
            oncall_sre(SCHEDULE_IDS)
        else:
            print 'unknown option: use wing | tindia'
            sys.exit(1)

if __name__ == '__main__':
     main()