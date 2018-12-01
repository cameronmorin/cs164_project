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
  
###FIXME should end here
s.close()

  # #ACK check
  # ack = s.recv(1024)
  # if ack != ('ACK' + str(numACK) + ': ' + choice):
  #   print ack
  #   print 'Error sending message: choice. Exiting...'
  #   sys.exit()
  # numACK = 1 - numACK

  # #Exit
  # if choice != '1':
  #   print 'Goodbye!'
  #   s.close()
  #   break

  # #Login loop
  # while (1):
  #   #Gather username and password
  #   username = raw_input('Please enter your username: ')
  #   password = getpass('Please enter your password: ')

  #   #Send username and password
  #   try:
  #     s.send(username)
  #     ack = s.recv(1024)
  #     if ack[:4] != 'ACK' + str(numACK):
  #       print 'Wrong ACK'
  #     numACK = 1 - numACK

  #     s.send(password)
  #     ack = s.recv(1024)
  #     if ack[:4] != 'ACK' + str(numACK):
  #       print 'Wrong ACK'
  #     numACK = 1 - numACK

  #   except socket.error, msg:
  #     print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
  #     sys.exit()

  #   #Receive server reply to validate login
  #   reply = s.recv(4096)
  #   if reply == 'Valid Login':
  #     break
  #   else:
  #     print 'Error: Invalid username or password.'

  # print 'Successful login!\n'
  
  # #Menu
  # while (1):
  #   #Print menu
  #   menu()
  #   function = raw_input('Please enter your choice: ')
  #   print ''

  #   try:
  #     s.send(function)
  #     ack = s.recv(1024)
  #     if ack[:4] != 'ACK' + str(numACK):
  #       print 'Wrong ACK'
  #     numACK = 1 - numACK

  #   except socket.error, msg:
  #     print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
  #     sys.exit()

  #   if function == 'Q':
  #     #Logout
  #     print 'Goodbye!\n'
  #     break

  #   elif function == 'P':
  #     #Change password
  #     while(1):
  #       newPassword = getpass('Please enter your new password:')
  #       verify = getpass('Please re-enter your new password:')
  #       if newPassword != verify:
  #         print 'Error: Passwords did not match. Please try again.'
  #       else:
  #         break
  #     s.send(newPassword)
  #     ack = s.recv(1024)
  #     if ack[:4] != 'ACK' + str(numACK):
  #       print 'Wrong ACK'
  #     else:
  #       print 'Password changed!\n'
  #     numACK = 1 - numACK

  #   else:
  #     print 'Invalid operation!!!\n'
      