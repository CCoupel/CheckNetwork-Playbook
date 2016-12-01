#!/usr/bin/python

import  socket, sys
from ansible.module_utils.basic import *
import httplib
import re
import time

BUFFER_SIZE = 1024

def TCP(IP, PORT, TIMEOUT, MESSAGE):
  data=""
  ERROR=""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Check if serveur is TCP UP
  try:
    s.settimeout(TIMEOUT)
    s.connect((IP, PORT))
    s.send(MESSAGE+"\n")
    while len(data) == 0:
      data = s.recv(BUFFER_SIZE)
      if not data: break
      print  data
  except socket.error as msg:
    if len(data) == 0:
      ERROR= "Couldnt connect with the socket-server: %s\n " % msg
      return True,False, data,ERROR

  s.shutdown(socket.SHUT_RDWR)
  s.close()
  return False,data!=MESSAGE, data,""

def UDP(IP, PORT, TIMEOUT, MESSAGE):
  data=""
  ERROR=""
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.settimeout(TIMEOUT)
    s.connect((IP, PORT))
    s.sendto(MESSAGE,(IP, PORT))
    while len(data) == 0:
      data = s.recv(BUFFER_SIZE)
      if not data: break
      print data
  except socket.error as msg:
    if len(data) == 0:
      ERROR= "Couldnt connect with the socket-server: %s\n " % msg
      return True,False, data,ERROR
      
  s.close()
  return False,data!=MESSAGE, data,ERROR

def HTTP(IP, PORT, TIMEOUT, URL):
  ERROR=""
  time.sleep(TIMEOUT)
  try:
    conn = httplib.HTTPConnection(IP, PORT, timeout=TIMEOUT)
    req=conn.request("HEAD", URL)
    resp=conn.getresponse()
  except Exception as msg:
    ERROR=str(msg)
    return True,False, "",ERROR

  #return False,re.match("^[23]\d\d$", str(resp.status))!=True, str(resp.reason)+re.match("^[23]\d\d$", "200")+".."+re.match("^[23]\d\d$", "400"),str(resp.status)
  return False,not(str(resp.status).startswith("2")|str(resp.status).startswith("3")), str(resp.reason),str(resp.status)

def main():
  fields = {
    "BindIP": {"required": True, "type": "str"},
    "Port": {"required": True, "type": "int"},
    "Message": {"default": "", "type": "str"},
    "Timeout": {"default": 5, "type": "int"},
    "Protocol": {
      "default": "tcp",
      "choices": ['tcp', 'udp','http'],
      "type": 'str',
    },
  }

  module = AnsibleModule(argument_spec=fields)

  result=False
  IP = module.params["BindIP"]
  PORT = module.params["Port"]
  PROTO=module.params["Protocol"]
  MESSAGE=module.params["Message"]
  TIMEOUT=module.params["Timeout"]


  if PROTO.upper() == "TCP":
    Failed, Changed, Out, Err=TCP(IP, PORT,TIMEOUT,MESSAGE)
  elif PROTO.upper() == "UDP":
    Failed,Changed, Out, Err=UDP(IP, PORT,TIMEOUT,MESSAGE)
  elif PROTO.upper() == "HTTP":
    Failed,Changed, Out, Err=HTTP(IP, PORT,TIMEOUT,MESSAGE)

  module.exit_json(changed=Changed,failed=Failed,stderr=Err, stdout=Out)

if __name__ == '__main__':
    main()
      
