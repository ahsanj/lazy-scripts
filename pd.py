#!/usr/bin/python
'''
usage: create a file called config.py in the same directory and add your PagerDuty API key
api_key= " "  

scripts takes one argument "xxx", "xxx" , "xxx" , "incident"

***schedules***
https://xxxx.pagerduty.com/schedules#xxxx - xxx
https://xxxx.pagerduty.com/schedules#xxxx - xxx
https://xxxx.pagerduty.com/schedules#xxxx - xxx

for Open incidents 'triggered' or 'acknowledged'
https://api.pagerduty.com/incidents#xxxxE' - incidents

'''
import requests
import json
import sys
import config
import logging
import datetime

#from argparse import ArgumentParser
#logging.basicConfig(filename='/var/log/pagerduty.log', level=logging.INFO, format='%(asctime)s,%(message)s')

API_KEY = config.api_key

TIME_ZONE = 'UTC'
#SRE_SCHEDULE_IDS = ['xxx']
#TI_SCHEDULE_IDS =['xxx']
#SCHEDULE_IDS= TI_SCHEDULE_IDS

def oncall_sre(SCHEDULE_IDS,queue):
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

    #logging.info('User='+new_data['user']['summary']+','+'Team='+ queue)
    print datetime.datetime.now().strftime("%d %B %I:%M:%S"),'User:'+new_data['user']['summary'], 'Team:'+queue
    
def list_incidents(SERVICE_IDS):
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=API_KEY)
    }
    payload = {
        'statuses[]': ['triggered', 'acknowledged'],
        'service_ids[]': SERVICE_IDS,
    }
    r = requests.get(url, headers=headers, params=payload)
    data=r.json()
    #print data["incidents"][0]["summary"]
    #print data
    open_incident=len(data["incidents"])
    print datetime.datetime.now().strftime("%d %B %I:%M:%S"),'Open incidents: '+str(open_incident)

def main():

    #parser = ArgumentParser(description='Print the name of the person who is oncall....'
    #			    'scripts takes one argument "wing", "cloudworks" or "gov" ',
    #                        epilog='Written by Ahsan Javed <ajaved@splunk.com>')
    #args = parser.parse_args()
    
    if len(sys.argv) == 1:
        print 'usage: ./pd.py {xxx | xxx | xxx | incidents}'
        sys.exit(1)
    if  sys.argv[1] == "xxx" or "xxx" or "xxxx" or "incidents":
        option = sys.argv[1]
        if option == 'xxx':
            SCHEDULE_IDS = ['xxxx']
            oncall_sre(SCHEDULE_IDS,option)
        elif option == 'xxx':
            SCHEDULE_IDS =['xxxx']
            oncall_sre(SCHEDULE_IDS,option)
        elif option == 'xxxx':
            SCHEDULE_IDS =['xxxx']
            oncall_sre(SCHEDULE_IDS,option)
        elif option == "incidents":
            SERVICE_IDS = ['xxx']
            list_incidents(SERVICE_IDS)
        else:
            print 'unknown option: use xxx | xxx | xxx | incidents'
            sys.exit(1)

if __name__ == '__main__':
     main()
