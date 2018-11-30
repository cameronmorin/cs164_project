import socket, sys
from thread import *

HOST = ''
PORT = 6035

connections = []
credentials = [['cam', '1234'], ['harley', 'rock'], ['john', 'pass']]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket Created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Error code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'


def clientthread(conn):
    numACK = 0

    while(1):
        #Receive landing page response
        initial = conn.recv(1024)
        ack = 'ACK' + str(numACK) + ': ' + initial
        conn.send(ack)
        numACK = 1 - numACK

        #Exit
        if initial != '1':
            print 'Removing connection with: ' + str(conn)
            connections.remove(conn)
            break
        
        #User sign-on
        while (1):
            #Receive username from client
            username = conn.recv(1024)
            ack = 'ACK' + str(numACK) + ': ' + username
            conn.send(ack)
            numACK = 1 - numACK

            #Receive password from client
            password = conn.recv(1024)
            ack = 'ACK' + str(numACK) + ': ' + password
            conn.send(ack)
            numACK = 1 - numACK

            login = [username, password]
            #Look for login in list
            try:
                cred = credentials.index(login)
                reply = 'Valid Login'
                conn.send(reply)
                break
            except ValueError:
                invalid = 'Invalid credentials. Please try again'
                conn.send(invalid)


        #Menu input
        while (1):
            data = conn.recv(1024)
            ack = 'ACK' + str(numACK) + ': ' + data
            conn.send(ack)
            numACK = 1 - numACK

            if (data[:1] == 'Q'):
                #Logout
                print 'Logout'
                break
            elif (data[:1] == 'P'):
                #Change Password
                newPassword = conn.recv(1024)
                print credentials[cred][1]
                credentials[cred][1] = newPassword
                print credentials[cred][1]
                ack = 'ACK' + str(numACK) + ': ' + data
                conn.send(ack)
                numACK = 1 - numACK
                
            else:
                if data == '':
                    print 'Connection loss in menu.'
                    connections.remove(conn)
                    conn.close()
                    return
                #Invalid operation
                print 'Invalid operation'
    
    conn.close()


while (1):
    conn, addr = s.accept()
    connections.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientthread ,(conn,))

s.close()