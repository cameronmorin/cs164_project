from getpass import getpass
import socket
import sys
import time

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error:
  print 'Failed to create socket.'
  sys.exit()

host = 'localhost'
port = 6035

try:
  remote_ip = socket.gethostbyname(host)
except socket.gaierror:
  print 'Hostname could not be resolved. Exiting'
  sys.exit()

s.connect((remote_ip, port))
print 'Socket connected to ' + host + ' on ip ' + remote_ip


#Login loop
while (1):
  #Gather username and password
  username = raw_input('Please enter your username: ')
  password = getpass('Please enter your password: ')
  
  #Send username
  try:
    s.sendall(username)
    time.sleep(1)
    s.sendall(password)

  except socket.error, msg:
    print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

  #Receive server reply to validate login
  reply = s.recv(4096)
  if reply == 'Valid Login':
    break
  else:
    print 'Error: Invalid username or password.'

print 'Successful login'
# while(1) :
#   msg = raw_input('Enter a test message: ')
  
#   try:
#     s.sendto(msg, (host, port))
    
#     d = s.recvfrom(1024)
#     reply = d[0]
#     addr = d[1]

#     print 'Server reply: ' + reply

#   except socket.error, msg:
#     print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
