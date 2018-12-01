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

def landingPage():
    page = 'Welcome to MiniBook\n'
    page += 'Login (1)\n'
    page += 'Exit (0)\n'
    return page

def menu():
    menu = '\nMenu\n'
    menu += 'Please choose an option:\n'
    menu += '1: Change Password (P)\n'
    menu += '2: Logout (Q)\n'
    return menu

def clientthread(conn):
    numACK = 0

    while(1):
        #Send landing page
        page = landingPage()
        conn.send(page)

        initial = conn.recv(1024)
        # ack = 'ACK' + str(numACK) + ': ' + initial
        # conn.send(ack)
        # numACK = 1 - numACK

        #Exit
        if initial != '1':
            print 'Removing connection with: ' + str(conn)
            connections.remove(conn)
            break
        
        #User sign-on
        while (1):
            #Receive username from client
            message = 'Please enter your username: -m'
            conn.send(message)
            username = conn.recv(1024)
            
            # ack = 'ACK' + str(numACK) + ': ' + username
            # conn.send(ack)
            # numACK = 1 - numACK
            
        
            #Receive password from client
            message = 'Please enter your password: -p'
            conn.send(message)
            password = conn.recv(1024)
            # ack = 'ACK' + str(numACK) + ': ' + password
            # conn.send(ack)
            # numACK = 1 - numACK

            login = [username, password]
            #Look for login in list
            try:
                cred = credentials.index(login)
                message = 'Welcome ' + credentials[cred][0] + '!-o'
                conn.send(message)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    print 'System error. Closing connection'
                    connections.remove(conn)
                    conn.close()
                    return
                break
            except ValueError:
                invalid = 'Invalid credentials. Please try again\n-o'
                conn.send(invalid)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    print 'System error. Closing connection'
                    connections.remove(conn)
                    conn.close()
                    return


        #Menu
        while (1):
            message = menu()
            conn.send(message)
            # ack = 'ACK' + str(numACK) + ': ' + data
            # conn.send(ack)
            # numACK = 1 - numACK

            data = conn.recv(1024)
            if (data[:1] == 'Q'):
                #Logout
                conn.send('Logging out...\n-o')
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    print 'System error. Closing connection'
                    connections.remove(conn)
                    conn.close()
                    return
                break
            elif (data[:1] == 'P'):
                #Change Password
                while(1):
                    message = 'Please enter new password: -p'
                    conn.send(message)
                    newPassword = conn.recv(1024)

                    message = 'Please re-enter your new password: -p'
                    conn.send(message)
                    verify = conn.recv(1024)

                    if newPassword == verify:
                        credentials[cred][1] = newPassword
                        message = 'Password change successful.\n-o'
                        conn.send(message)
                        #Print ACK from client
                        ack = conn.recv(1024)
                        if ack != 'ACK':
                            print 'System error. Closing connection'
                            connections.remove(conn)
                            conn.close()
                            return
                        break
                    else:
                        message = 'Passwords did not match. Please try again\n-o'
                        conn.send(message)
                        #Print ACK from client
                        ack = conn.recv(1024)
                        if ack != 'ACK':
                            print 'System error. Closing connection'
                            connections.remove(conn)
                            conn.close()
                            return
                # print credentials[cred][1]
                # credentials[cred][1] = newPassword
                # print credentials[cred][1]
                # ack = 'ACK' + str(numACK) + ': ' + data
                # conn.send(ack)
                # numACK = 1 - numACK
                
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