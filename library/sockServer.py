#!/usr/bin/python
import sys, socket
from ansible.module_utils.basic import *
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer




BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
 
def TCP(IP, PORT)  :
  data=""
  tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  try:
    tcp.bind((IP, PORT))
  except socket.error as msg:
    print "Couldnt connect with the socket-server: %s\n terminating program" % msg
    return True,"",msg
  tcp.listen(1)
 
  conn, addr = tcp.accept()
  print 'Connection address:', addr
  while len(data) == 0:
    Failed=False
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received TCP data:", data
    conn.send(data)  # echo
  conn.close()
  return False,data, ""
 
def UDP(IP,PORT):
  data=""
  udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    udp.bind((IP, PORT))
  except socket.error as msg:
    print "Couldnt connect with the socket-server: %s\n terminating program" % msg
    return True, "", msg
  while len(data) == 0:
    Failed=False
    data, addr = udp.recvfrom(8000)
    if not data: break
    print "Recv UDP data:'%s'" % data
    udp.sendto(data,addr)
  udp.close()
  return False,data,""
 





class always200Handler(BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("Jeronimo!")
    return False,"",""

def HTTP(IP,PORT):
  server_address = (IP, PORT)
  try:
    httpd=HTTPServer(server_address,always200Handler)
    httpd.serve_forever()
  except Exception as msg:
    httpd.socket.close()
  return False, "",""


def main():
  fields = {
    "BindIP": {"default": "0.0.0.0", "type": "str"},
    "Port": {"required": True, "type": "int"},
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
 
  if PROTO.upper() == "TCP":
    result, data, msg=TCP(IP, PORT)
  elif PROTO.upper() == "UDP":
    result,data, msg=UDP(IP, PORT)
  elif PROTO.upper() == "HTTP":
    result,data, msg=HTTP(IP, PORT)

  module.exit_json(changed=False,failed=result, stderr=str(msg), stdout=str(data) )

if __name__ == '__main__':
    main()
