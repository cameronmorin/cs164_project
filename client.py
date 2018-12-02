from getpass import getpass
import socket
import sys
import time

host = 'localhost'
port = 6035
numACK = 0

def menu():
    # menu = 'Welcome to the server!\n'
    menu = 'Please choose an option:\n'
    menu += '1: Change Password (P)\n'
    menu += '2: Logout (Q)\n'
    print menu
    return

#Create socket
try:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
  print 'Failed to create socket.'
  sys.exit()
#Get server IP
try:
  remote_ip = socket.gethostbyname(host)
except socket.gaierror:
  print 'Hostname could not be resolved. Exiting'
  sys.exit()
#Connect to the server IP
s.connect((remote_ip, port))
print 'Socket connected to ' + host + ' on ip ' + remote_ip + '\n'


#Main loop
while (1):
  # landingPage = 'Welcome to MiniBook\n'
  # landingPage += 'Login(1)\n'
  # landingPage += 'Exit(0)\n'
  # print landingPage

  server = s.recv(1024)
  
  if server == '':
    #Server closed the connection
    print 'Goodbye!'
    break
  elif server[-2:] == '-o':
    #Server output statement
    print server[:-2]
    choice = 'ACK'
  elif server[-2:] == '-p':
    #Server sends the getpass flag
    choice = getpass(server[:-2])
  elif server[-2:] == '-u' or server[-2:] == '-m':
    #Server sends the username or message flag
    choice = raw_input(server[:-2])
  else:
    print server
    choice = raw_input('Please enter your choice: ')

  s.send(choice)
  
s.close()