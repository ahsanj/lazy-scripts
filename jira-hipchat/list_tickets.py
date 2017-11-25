from jira import JIRA
import requests
import sys
from urlparse import urljoin
import config
import string


def list_tickets():

    try:
        jira = JIRA(basic_auth=(config.username, config.password), options={'server': config.server })
        query = 'project = CO AND status not in (Waiting, "In Review", Closed) AND assignee is empty AND component in \
        (deployment, incident, SRE) AND ("Stack ID" not in (cis, cdt-eng) OR "Stack ID" is EMPTY)\
        ORDER BY cf[12801] ASC'
    except:
        print "Check your credentials"
        sys.exit()

    issues = jira.search_issues(query, maxResults=100)
    count = 0
    tickets=[]
    for issue in issues:
          #print issue, issue.fields.duedate, issue.fields.assignee
        count +=1
        issue =str(issue)
        url = urljoin(config.queue,issue)
        tickets.append(url)
    text= '\n'.join(tickets)
    return text

'''
curl -d '{"color":"green","message":"I can send message","notify":false,"message_format":"text"}'
-H 'Content-Type: application/json'
https://hipchat.xxxxx.com/v2/room/9604/notification?auth_token=e,kfhelfhelfhelwfh
'''

def send_msg(tickets):

    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('auth_token', config.token),
    )

    total_tickets= str(len(tickets.split('\n')))

    #message= str(message.split(' '))
    tickets = str(tickets.splitlines(True))
    tickets_cleaned = string.replace(tickets[1:-1], ',', '')
    message = string.replace(tickets_cleaned, "'", "")
    #print message

    data = '{"color":"green","message":"@here The total number of unassigned ticket(s) in SRE Staff Queue is '+total_tickets+'\
    \\n Tickets:\\n'+message+'","notify":false,"message_format":"text"}'

    req= requests.post(config.hipchat, headers=headers, params=params, data=data)

    if req.status_code not in range(200, 300):
        print "Request didnt go through, status returned: ",req.status_code
    else:
        print "Request accepted: ",req.status_code



def main():

    tickets= list_tickets()
    send_msg(tickets)

if __name__ == '__main__':
    main()
