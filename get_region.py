#!/usr/bin/python
import json
import git
import sys
import os

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    IMP = '\033[91m'
    ENDC = '\033[0m'

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
        with open("stax/"+stack+".json",'r') as json_data:
            data = json.load(json_data)
            #print data
            print "\nThis Stack is deployed in:", bcolors.WARNING + data["attributes"]["cloud_region"] + bcolors.ENDC
            print " "
        return data
    except:
        print "This PO", stack , "does not exists "
        sys.exit()

def get_stack_details(stack_data):
    #print stack_data["compute"]
    try:
        if stack_data["attributes"]["splunkwhisper"]["encryption"]["dsm"] != " ":
            print bcolors.IMP + "*** This is a Vormetric stack! *** "  + bcolors.ENDC
    except:
            print  bcolors.OKGREEN +  "Non vormetric Stack" + bcolors.ENDC

    sversion=stack_data["attributes"]["splunkwhisper"]["splunk_version"]
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


def main():
    git_pull()
    jdata=get_region()
    get_stack_details(jdata)

if __name__ == '__main__':
    main()
