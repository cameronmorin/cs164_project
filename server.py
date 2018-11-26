import socket
import sys
from thread import *

HOST = ''
PORT = 6035
connections = []
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket Created'
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))

except socket.error , msg:
  print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
  sys.exit()

print 'Socket bind complete'

s.listen(5)
print 'Socket now listening'

def clientthread(conn):
  conn.send('Welcome to the server. Type something and hit enter\n')

  while True:
    data = conn.recv(1024)
    if (data[:2] == '!q'):
      break
    elif (data[:9] == '!sendall '):
      reply = data[9:]
      for item in connections:
        item.sendall(reply)
    else:
      reply = 'OK...' + data
      if not data:
        break
      conn.sendall(reply)


  conn.close()

while (1):
  conn, addr = s.accept()
  connections.append(conn)
  print 'Connected with ' + addr[0] + ':' + str(addr[1])

  start_new_thread(clientthread ,(conn,))

s.close()