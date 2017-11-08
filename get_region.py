import json
import git
import sys
import os


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
            print data["attributes"]["cloud_region"]
    except:
        print "This PO", stack , "does not exists "
        sys.exit()

def main():
    git_pull()
    get_region()

if __name__ == '__main__':
    main()
