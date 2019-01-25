#!/usr/bin/python3

import time
import socket
import subprocess as s
import time
from datetime import datetime
import _thread

now_UTC = datetime.utcnow() # Get the UTC time
starttime=time.time()
ip_dict = {
    "zoomhash.io" : 0,
    "airportshops.ddns.net" : 0,
    "entiat.ddns.net" : 0,
    "division.ddns.net" : 0,
    "columbia.ddns.net" : 0
}    
port_dict = {
    "zoomhash.io" : 80,
    "airportshops.ddns.net" : 22,
    "entiat.ddns.net" : 22,
    "division.ddns.net" : 710,
    "columbia.ddns.net" : 710
}    

def try_port_22(ip_address):
    port = port_dict[ip_address]
    # Start socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Force socket to connect to TCP port
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # set the timeout to .2 seconds
    s.settimeout(0.2)
    try:
        s.connect((ip_address, port))
    except socket.timeout:
    # Timed out
        print("TIMEOUT FOR: " + ip_address + str(port))
        s.close()
        return False
    except socket.error:
        # Couldn't connect to the address on that port
        print('Failed to connect')
        s.close()
        return False
    else:
        print ('Looks Like ' + ip_address + str(port) + ' is OK')
        return True
    s.close()
    
def send_message_to_slack(text):
    from urllib import request, parse
    import json

    post = {"text": "{0}".format(text)}

    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                            data=json_data.encode('ascii'),
                            headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

def are_you_up(ip_address):
    control = False
    while control == False:
        ip_dict[ip_address] = 0
        time.sleep(5)
        if try_port_22(ip_address) == True:
            send_message_to_slack(now_UTC + '--Ping Is Back UP For: ' + ip_address)
            control = True
    return 0

while True:
    for ip, count in ip_dict.items():
        if try_port_22(ip) == False:
            ip_dict[ip] += 1
            if ip_dict[ip] > 2:
                send_message_to_slack(now_UTC + '--Theres An Outage At ' + ip + ' Site' + 'port: ' + port_dict[ip])
                ip_dict[ip] = 0
                _thread.start_new_thread( are_you_up, (ip, ) )
        else:
            ip_dict[ip] = 0
    time.sleep(30)
    if now_UTC.minute > 59:
        for each in ip_dict:
            ip_dict[each] = 0

#time.sleep(60.0 - ((time.time() - starttime) % 60.0))