import socket, sys, hashlib
from thread import *
from user import User

HOST = ''
PORT = 6035

connections = []
cam = User('cam', '99fb2f48c6af4761f904fc85f95eb56190e5d40b1f44ec3a9c1fa319')
harley = User('harley', '6f1bed21dd4f3e7c3f0fc3c4152126fe3e9e6bcabb2610aa3d645549')
john = User('john', 'ccc9c73a37651c6b35de64c3a37858ccae045d285f57fffb409d251d')
users = [cam, harley, john]

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
    menu += '3: Send message (M)\n'
    return menu

def ackError(conn, user):
    print 'System error. Closing connection'
    user.connection = 0
    user.onlineStatus = 0
    connections.remove(conn)
    conn.close()

def sendMessage(sender):
    toSend = '\n===========\n'
    toSend += 'FROM: ' + sender + '\n'
    return toSend

def printUnreadMessages(user, flag):
    toSend = 'You have received ' + str(len(user.unreadMessages)) + ' new messages\n'
    for msg in user.unreadMessages:
        toSend += sendMessage(msg[0])
        toSend += msg[1]
    toSend += '-o'
    return toSend


def clientthread(conn):
    # numACK = 0

    while(1):
        flag = 0                #Flag to denote unread messages on login

        #Send landing page
        page = landingPage()
        conn.send(page)

        initial = conn.recv(1024)

        #Exit
        if initial != '1':
            print 'Removing connection with: ' + str(conn)
            connections.remove(conn)
            break
        
        validCred = False
        #User sign-on
        while validCred == False:
            #Receive username from client
            message = 'Please enter your username: -m'
            conn.send(message)
            username = conn.recv(1024)    
        
            #Receive password from client
            message = 'Please enter your password: -p'
            conn.send(message)
            password = conn.recv(1024)

            hashPass = hashlib.sha224(password).hexdigest()

            #Look for login in list
            for user in users:
                if user.username == username and user.password == hashPass:
                    #Set current user
                    currentUser = user
                    #Set user's online status to online
                    currentUser.onlineStatus = 1
                    #Set current user's connection
                    currentUser.connection = conn

                    message = '\nWelcome ' + user.username + '!-o'
                    conn.send(message)
                    #Print ACK from client
                    ack = conn.recv(1024)
                    if ack != 'ACK':
                        ackError(conn, currentUser)
                        return
                    validCred = True
                    break
            
            if validCred == False:
                invalid = 'Invalid credentials. Please try again\n-o'
                conn.send(invalid)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
                    return
                

        #Notify user of unread messages on sign-in
        if len(currentUser.unreadMessages) > 0:
            #Print number of unread messages
            flag = 1
            message = 'You have ' + str(len(currentUser.unreadMessages)) + ' new messages:\n-o'
            conn.send(message)
            ack = conn.recv(1024)
            if ack != 'ACK':
                ackError(conn, currentUser)

        #Menu
        while (1):
            #FIXME Check if the user received any messages in real time
            if len(currentUser.unreadMessages) > 0:
                if flag == 0:
                    toSend = printUnreadMessages(currentUser, flag)
                    currentUser.unreadMessages = []
                    conn.send(toSend)
                    #Print ACK from client
                    ack = conn.recv(1024)
                    if ack != 'ACK':
                        ackError(conn, currentUser)

            #Send menu
            message = menu()
            conn.send(message)

            data = conn.recv(1024)
            if (data[:1] == 'Q'):
                #Logout
                conn.send('Logging out...\n-o')

                #Set status back to offline
                currentUser.onlineStatus = 0

                #Set connection back to 0
                currentUser.connection = 0

                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
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
                        currentUser.changePassword(hashlib.sha224(newPassword).hexdigest())
                        message = 'Password change successful.\n-o'
                        conn.send(message)
                        #Print ACK from client
                        ack = conn.recv(1024)
                        if ack != 'ACK':
                            ackError(conn, currentUser)
                            return
                        break
                    else:
                        message = 'Passwords did not match. Please try again\n-o'
                        conn.send(message)
                        #Print ACK from client
                        ack = conn.recv(1024)
                        if ack != 'ACK':
                            ackError(conn, currentUser)
                            return
            elif (data[:1] =='M'):
                #Send message
                message = 'Please enter your message: -m'
                conn.send(message)
                messageToSend = conn.recv(1024)

                message = 'Please enter the username of the recipient: -u'
                conn.send(message)
                recip = conn.recv(1024)

                for user in users:
                    if user.username == recip:
                        user.unreadMessages.append([currentUser.username, messageToSend])
                        # if user.onlineStatus == 0:
                        #     #Recipient is offline
                        #     user.unreadMessages.append([currentUser.username, messageToSend])
                        # else:
                        #     #Recipient is online
                        #     messageToSend += '-o'       #Add display only flag
                            
                        #     message = sendMessage(currentUser.username) + messageToSend
                        #     #send the message out on the recipient connection
                        #     user.connection.send(message)
                        #     #Print ACK from client
                        #     ack = user.connection.recv(1024)
                        #     # if ack != 'ACK':
                        #     #     ackError(user.connection, user)
                        break
                
                #Message sent
                message = 'Message delivered to: ' + recip + ' successfully!\n-o'
                conn.send(message)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
                    return
            elif data == 'ACK':
                continue
            else:
                if data == '':
                    print 'Connection loss in menu.'
                    ackError(conn, currentUser)
                    return
                #Invalid operation
                print 'Invalid operation'
                ackError(conn, currentUser)
    
    conn.close()


while (1):
    conn, addr = s.accept()
    connections.append(conn)
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    start_new_thread(clientthread ,(conn,))

s.close()