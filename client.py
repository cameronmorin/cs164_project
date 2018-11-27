from getpass import getpass
import socket
import sys

try:
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except socket.error:
  print 'Failed to create socket.'
  sys.exit()

host = 'localhost'
port = 6035

try:
  remote_ip = socket.gethostbyname(host)
except socket.error, msg:
  print 'Hostname could not be resolved. Exiting'
  sys.exit()

s.connect((host, port))
print 'Socket connected to ' + host + ' on ip ' + remote_ip

while (1):
  #Gather username and password
  username = raw_input('Please enter your username: ')
  password = getpass('Please enter your password: ')
  try:
    s.sendall(username)
    s.sendall(password)

  except socket.error, msg:
    print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

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
