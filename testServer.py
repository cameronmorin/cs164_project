import socket
import sys

HOST = ''
PORT = 8888

logins = [('cam', '1234'), ('john', 'pass'), ('andrew', 'yeet'), ('harley', 'rock')]




try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' Message ' + str(msg[1])
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + str(msg[1])
    sys.exit()

print 'Socket bind complete.'

currACK = 0

while (1):
    # receive data from the client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    code = data[1]

    if code == 1:
        #User login
        cred = data[0]
        try:
            login = logins.index(cred)
            s.sendto('Valid Login', addr)
        except ValueError:
            s.sendto('Invalid Login', addr)

    # if currACK == 0:
    #     reply = 'ACK0: OK...' + data
    #     currACK = 1
    # else:
    #     reply = 'ACK1: OK...' + data
    #     currACK = 0
        
    # s.sendto(reply, addr)
    # print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()