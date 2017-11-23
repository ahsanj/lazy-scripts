#!/usr/bin/python

import json
import git
import sys
import urllib2

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    IMP = '\033[91m'
    ENDC = '\033[0m'

def check_network():
    try:
        urllib2.urlopen('http://splunk.com', timeout=1)
        return True
    except urllib2.URLError as err:
        print "Oh look! The Internet is Down!"
        sys.exit()

def git_pull():
    try:
        print "Pulling the Stax Repo... "
        repo = git.cmd.Git('stax')
        repo.pull()
    except:
        print "Stax repo is not in your path "
        sys.exit()

def get_region():
    stack = raw_input("Enter the stack name: ")
    #print stack
    #print os.path.isfile("stax/"+stack+".json")
    try: 
        if not stack:
            raise ValueError('empty string')
    except:
        print "You did not enter the Stack name"
        sys.exit()
           
    try:
        with open("stax/"+stack+".json",'r') as json_data:
            data = json.load(json_data)
            #print data
            print "\nThis Stack is deployed in:", bcolors.WARNING + data["attributes"]["cloud_region"] + bcolors.ENDC
            print " "
        return data
    except:
        print "This PO", stack , "does not exists "
        sys.exit()

def check_vormetric(stack_data):
    try:
        if stack_data["attributes"]["splunkwhisper"]["encryption"]["dsm"] != " ":
            print bcolors.IMP + "*** This is a Vormetric stack! *** "  + bcolors.ENDC
            #print stack_data
            for host in stack_data["compute"]:
                if not "filesystem" in stack_data["compute"][host]["lvm"]:
                    print "This Instance is missing the filesystem field", bcolors.IMP + host + bcolors.ENDC
                if not "ami" in stack_data["compute"][host] and host !="c0m1" and host !="lm1":
                    print "This Instance is missing the AMI field ------", bcolors.IMP + host  + bcolors.ENDC

    except:
            print  bcolors.OKGREEN +  "Non vormetric Stack" + bcolors.ENDC


def get_stack_details(stack_data):
    #print stack_data["compute"]

    sversion=stack_data["attributes"]["splunkwhisper"]["splunk_version"]
    print " "
    print bcolors.OKGREEN + "Splunk version =>",sversion + bcolors.ENDC
    print " "

    count = 0
    print "-------------------------------------------------------------------"
    print "Re-provisioning for the follwoing instance(s) are set to 'allow' in PO"
    print "-------------------------------------------------------------------"
    template = "  {0:8}    {1:10} "
    print bcolors.OKGREEN + template.format("Instance","Re-provision") + bcolors.ENDC
    for host in stack_data["compute"]:
        count +=1
        if stack_data["compute"][host]["reprovision"] == "allow":
            print "-",host, bcolors.IMP + "re-provisioning for this instance is allowed" + bcolors.ENDC
            #print "\nTotal Instance count for this stack is:", count
            print "-","Instance type:", stack_data["compute"][host]["instance_type"] 

def main():
    print   bcolors.IMP + "*** If you have not pushed your changes to stax repo... you are not getting the right information ***" + bcolors.ENDC
    print " "
    #check_network()
    git_pull()
    jdata=get_region()
    check_vormetric(jdata)
    get_stack_details(jdata)

if __name__ == '__main__':
    main()
