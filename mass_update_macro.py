#!/usr/bin/env python
###########################################
# Zabbix Auto disable/enable trigger script
# Call Zabbix API
###########################################
# ChangeLog:
# 20160729    TZ initial creation
###########################################
import sys
import getpass
import os

sys.path.append('./lib')

from zabbix_api import ZabbixAPI, ZabbixAPIException

url = 'XX'
HostListFile = '/home/zabbix/conf/host_list'
zapi = ZabbixAPI(server=url)

WARNING = '\033[93m'
ENDC = '\033[0m'
def Login():
    try:
        zapi.login(Username, Password)
    except ZabbixAPIException, e:
        print("Error:Name or Password is wrong")
        print e
        sys.exit(1)

def fetchList():
    r = open(HostListFile).read()
    return r.splitlines()

def parseList(HostList):

    try:
        detail = HostList.split()
        hostName = detail[0]
    except Exception as e:
        print "Error while processing: %s" % HostList 
        print e
        return
    
    return (hostName)

def checkHostId(hostName):

    result = zapi.host.get({"filter":{"host":[hostName]},"output":"hostid"})
    if not result:
        return
    else:
        return result[0]['hostid']


def updateMacro(hostId, macroName, macroValue):

    try:
        zapi.host.update({"hostid": hostId,"macros": [{"macro":macroName,"value":macroValue}]})
    except ZabbixAPIException, e:
        print ("Error:Zabbix Update Macro %s on Host %s Failed!!") % (macroName, hostId)
        print("Additional info: %s") % e

def inputInfo():

    while True:
        Username = raw_input("Please input Zabbix user name:")
        if not Username:
            print WARNING + "Warn: User name is empty" + ENDC
            continue
        else:
            break

    while True:
        Password = getpass.getpass("Please input Zabbix password:")
        if not Password:
            print WARNING + "Warn: password is empty" + ENDC
            continue
        else:
            break

    while True:
        macroName = raw_input("Please input macro name:")
	if not macroName:
	    print WARNING + "Warn: Macro name is empty" + ENDC
	    continue
	else:
	    break

    while True:
	macroValue = raw_input("Please input macro value:")
	if not macroValue:
            print WARNING + "Warn: Macro Value is empty" + ENDC 
            continue
	else:
	    break
    return (Username, Password, macroName, macroValue)
    

def main():
    if not os.path.exists(HostListFile):
        print 'Missing trigger list file: %s' % HostListFile
        sys.exit(1)

    for line in fetchList():
        if str(line)[0] == '#':
            continue

        hostName = parseList(line)
        hostId = checkHostId(hostName) 
        if not hostId:
            print WARNING + "[%s]:: Host does not exist!!!" % hostName + ENDC
            continue
        else:
            updateMacro(hostId, macroName, macroValue)
            print "[%s]:: Successfully update macro %s to %s" % (hostName, macroName, macroValue)

if __name__=='__main__':
    Username, Password, macroName, macroValue=inputInfo()
    Login()
    main()
