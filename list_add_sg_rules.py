#!/usr/bin/python

import boto3
from argparse import ArgumentParser
import sys
import re

'''
{u'IpPermissionsEgress': [{u'IpProtocol': '-1', u'PrefixListIds': [], u'IpRanges': [{u'CidrIp': '0.0.0.0/0'}], u'UserIdGroupPairs': [],
u'Ipv6Ranges': []}], u'Description': 'launch-wizard-1 created', u'IpPermissions': [{u'PrefixListIds': [],
u'FromPort': 22, u'IpRanges': [{u'CidrIp': '0.0.0.0/0'}], u'ToPort': 22, u'IpProtocol': 'tcp', u'UserIdGroupPairs': [], u'Ipv6Ranges': 
[]}], u'GroupName': 'ahsantest', u'VpcId': 'xxxxxxx', u'OwnerId': '93xxxxx', u'GroupId': 'xxxxxx'}, 
'''

def total_sgs():
    
    total_sg=0
    sgs= ec2.describe_security_groups()['SecurityGroups']
    for sg in sgs:
        count = count +1
    print 'The total no of Security Groups in this region is:',total_sg

def sg_rules(stack,region):
    
    print "\nGetting the %s SG rules" %stack
    print ""
    count = 0
    count1 = 0
    for name in boto3.client("ec2",region_name=region).describe_security_groups()['SecurityGroups']:
        #print name
        if name['GroupName'] == stack:
            g_id=name['GroupId']
            print '  Port \t\t\tCidr'
            for rule in name['IpPermissions']:
                count +=1
                #total_rules +=1
                if rule['FromPort'] ==  0 or rule['FromPort'] == 1:
                    print ' ','1 - 65535'
                else:
                    if len(rule['IpRanges']) > 1:
                        for x in rule['IpRanges']:     
                            print ' ',rule['FromPort'],'\t\t\t',rule['IpRanges'][0]['CidrIp']
                    else:
                        print ' ',rule['FromPort'],'\t\t\t',rule['IpRanges'][0]['CidrIp']
            #print '\nTotal no of rules in this security group %s is:' %stack,count
            #print "\nYou can add another", 50 - count, 'rules to', stack
            print ''
            return g_id
    else: 
        print "cannot find the stack!"
        sys.exit()
        
            

def add_rules(region,id):
    #print region, id
    add_exit = raw_input("If you want to add more rules to SG press any key otherwise no: ") 
    if add_exit == "no":
        sys.exit()
    else: 
        prot=  raw_input("Enter the IP Protocol e.g tcp/udp: ")
        ip_regex = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/(0|16|24|32)$")
        cidr=  raw_input("Enter the Cidr range e.g IPaddress/subnet<0.0.0.0/0> 0r <192.168.0.1/24>: ")
        ip_test = ip_regex.match(cidr)
        if ip_test:
            print "Acceptable ip address | Cidr block"
        else:
            print "Unacceptable ip address"
            sys.exit()
        
        for i in range(0,2):
            fport= raw_input("Enter the From port: ")
            try:
                checking_fport = int(fport)
            except ValueError:
                print "To Port should be digits only! "
                continue
            else:
                break
        
        for i in range(0,2):
            tport= raw_input("Enter the To port: ")
            try:
                checking_tport = int(tport)
            except ValueError:
                print "To Port should be digits only! "
            else:    
                break
	    #sys.exit()
        
        try:
            boto3.client("ec2",region_name=region).authorize_security_group_ingress\
            (GroupId=id,IpProtocol=prot, CidrIp=cidr, FromPort=int(fport), ToPort=int(tport))
        except:
            "print rule already exits in the SG"
    


def main():
    
    parser = ArgumentParser(description='Print and add the rules to exisitg AWS security group.... ' 
                                        'Add stack and the AWS region when prompted',
                            epilog='Written by Ahsan Javed <ajaved@splunk.com>')
    #parser.add_argument('--sg', help='Enter the Security Group name when prompted', required=True)
    #parser.add_argument('--region', help='Enter the AWS region when prompted', required=True)
    args = parser.parse_args()

    stack =raw_input ("Enter the stack name: ")
    try:
        if not stack:
            raise ValueError('empty string')
    except:
        print "Stack name! cannot be left blank"
        sys.exit()
    
    regions=['us-west-1','us-east-1','ap-northeast-1','ap-southeast-2','sa-east-1','ap-northeast-2',
             'us-east-2','ap-southeast-1','ca-central-1','cn-north-1','us-west-2','us-gov-west-1',
             'ap-south-1','eu-central-1','eu-west-1','eu-west-2']

    region = raw_input("Enter the AWS region e.g.(us-east-1): ")
    if region not in regions:
        print "Not a valid region"
        sys.exit()
    
    g_id=sg_rules(stack,region)
    add_rules(region,g_id)
    
if __name__ == '__main__':
    main()
