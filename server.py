import socket, sys
from thread import *

HOST = ''
PORT = 6035
connections = []

credentials = [('cam', '1234'), ('harley', 'rock'), ('john', 'pass')]

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
    # conn.send('Welcome to the server.')

    #User sign-on
    while (1):
        username = conn.recv(1024)
        print 'uname received: ' + username
        password = conn.recv(1024)
        print 'pass received ' + password
        login = (username, password)
        try:
            cred = credentials.index(login)
            reply = 'Valid Login'
            conn.sendall(reply)
            break
        except ValueError:
            invalid = 'Invalid credentials. Please try again'
            conn.sendall(invalid)
    
    print login
    print cred
    userMenu = menu()
    conn.sendall(userMenu)

    #Menu input
    while (1):
        data = conn.recv(1024)
        if (data[:1] == 'Q'):
            #Logout
            break
        elif (data[:1] == 'P'):
            #Change Password
            print cred
        else:
            reply = 'OK...' + data
            if not data:
                break
            conn.sendall(reply)
    
    conn.close()

def menu():
    menu = 'Welcome to the server!\n'
    menu += 'Please choose an option:\n'
    menu += '1: Change Password (P)\n'
    menu += '2: Logout (Q)\n'
    return menu

while (1):
    conn, addr = s.accept()
    connections.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientthread ,(conn,))

s.close()