import os
import re
import time
import sys
import nmap
import json

import psutil

'''
while True:
    ip = "192.168.1.2"
    response = os.popen(f"ping -n 1 {ip}").read()

    if "Destination host unreachable" in response or "Request timed out" in response:
        print("DOWN {} Ping Unsuccessful".format(ip))

    else:
        print("UP {} Ping Successful".format(ip))
    time.sleep(1)
    print(response)
    sys.stdout.flush()

'''

def upHostsList(network):
    nm = nmap.PortScanner()
    nm.scan(network, '22-443')
    return nm.all_hosts()
def filterPing(result):
    bytes = 0
    time = 0
    ttl = 0
    if "Destination host unreachable." in result or "Request timed out." in result:
        return {"status": "down", "bytes":bytes, "time":time, "ttl":ttl }
    else:
        result = result.split("\n")[2].split(" ")
        bytes = int(re.search(r'\d+', result[3]).group())
        time = int(re.search(r'\d+', result[4]).group())
        ttl = int(re.search(r'\d+', result[5]).group())
        return {"status":"up", "bytes":bytes, "time":time, "ttl":ttl }

def ping(ip):
    response = os.popen(f"ping -n 1 {ip} -w 1000").read()
    return response

def pingList(ipList):
    resultDict = {}
    for ip in ipList:
        resultDict[ip] = filterPing(ping(ip))
    return resultDict

def writeJSON(filename, data):
    json_object = json.dumps(data)
    with open(filename, "w") as outfile:outfile.write(json_object)

def readJSON(filename):
    with open(filename, 'r') as openfile: json_object = json.load(openfile)
    return json_object


def serverUptime():
    uptime = time.time() - psutil.boot_time()
    days = int(uptime/60/60/24%24)
    hours = int(uptime/60/60%24)
    minutes = int(uptime/60%60)
    seconds = int(uptime%60)
    return {'days': days, 'hours': hours, 'minutes': minutes, 'seconds': seconds}


def getCpuUsage(interval):
    return psutil.cpu_percent(interval)

def getRamInfo():
    percentage =  psutil.virtual_memory()[2]
    totalMemory = psutil.virtual_memory().total/1000000
    return {"Percentage":percentage, "totalMemory":totalMemory}


test = psutil.Process()
print(test.nice(10))



