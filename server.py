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
    page += '1: Login\n'
    page += '0: Exit\n'
    return page

def menu():
    menu = '\nMenu\n'
    # menu += 'Please choose an option:\n'
    menu += '1: Change Password\n'
    menu += '2: Send message\n'
    menu += '3: Read unread messages\n'
    menu += '4: Send broadcast message\n'
    menu += '5: See Friends\n'
    menu += '6: Send friend request\n'
    menu += '7: Respond to friend requests\n'
    menu += '0: Logout\n'
    return menu

def ackError(conn, user):
    print 'System error. Closing connection'
    user.connection = 0
    user.onlineStatus = 0
    connections.remove(conn)
    conn.close()

def sendMessage(sender):
    toSend = '-----------\n'
    toSend += 'FROM: ' + sender + '\n'
    return toSend

#FIXME Make a user class function
def printUnreadMessages(user):
    if len(user.unreadMessages) > 1:
        toSend = 'You have ' + str(len(user.unreadMessages)) + ' unread messages:\n'
    else:
        toSend = 'You have 1 unread message:\n'

    for msg in user.unreadMessages:
        toSend += sendMessage(msg[0])
        toSend += msg[1]
    toSend += '-o'
    return toSend

#FIXME Make a user class function
def printNewMessages(user):
    if len(user.newMessages) > 1:
        toSend = 'You have ' + str(len(user.newMessages)) + ' new messages:\n'
    else:
        toSend = 'You have 1 new message:\n'
    
    for msg in user.newMessages:
        toSend += sendMessage(msg[0])
        toSend += msg[1]
    toSend += '-o'
    return toSend

def clientthread(conn):
    # numACK = 0

    while(1):
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
            message = 'You have ' + str(len(currentUser.unreadMessages)) + ' unread messages.\n-o'
            conn.send(message)
            ack = conn.recv(1024)
            if ack != 'ACK':
                ackError(conn, currentUser)

        #FIXME Implement friend request notification
        if len(currentUser.friendRequests) > 0:
            message = 'You have ' + str(len(currentUser.friendRequests)) + ' friend requests awaiting decision.\n-o'
            conn.send(message)
            ack = conn.recv(1024)
            if ack != 'ACK':
                ackError(conn, currentUser)
        #Menu
        while (1):
            #FIXME Check if the user received any messages in real time
            if len(currentUser.newMessages) > 0:
                toSend = printNewMessages(currentUser)
                currentUser.newMessages = []
                conn.send(toSend)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)

            #Send menu
            message = menu()
            conn.send(message)

            data = conn.recv(1024)
            if (data[:1] == '0'):
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
            elif (data[:1] == '1'):
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
            elif (data[:1] =='2'):
                #Send message
                message = 'Please enter your message: -m'
                conn.send(message)
                messageToSend = conn.recv(1024)

                message = 'Please enter the username of the recipient: -u'
                conn.send(message)
                recip = conn.recv(1024)

                for user in users:
                    if user.username == recip:
                        if user.onlineStatus == 0:
                            #The user is offline
                            user.unreadMessages.append([currentUser.username, messageToSend])
                        else:
                            #The user is online
                            user.newMessages.append([currentUser.username, messageToSend])
                        break
                
                #Message sent
                message = 'Message delivered to: ' + recip + ' successfully!\n-o'
                conn.send(message)
                #Print ACK from client
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
                    return
            elif (data[:1] == '3'):
                #Read unread messages
                if len(currentUser.unreadMessages) > 0:
                    toSend = printUnreadMessages(currentUser)
                    currentUser.unreadMessages = []
                    conn.send(toSend)
                    #Print ACK from client
                    ack = conn.recv(1024)
                    if ack != 'ACK':
                        ackError(conn, currentUser)
                else:
                    #No unread messages
                    toSend = 'You have no unread messages at this time.\n -o'
                    conn.send(toSend)
                    #Print ACK from client
                    ack = conn.recv(1024)
                    if ack != 'ACK':
                        ackError(conn, currentUser)
            elif (data[:1] == '4'):
                #Broadcast message
                message = 'Please enter your message: -m'
                conn.send(message)
                messageToSend = conn.recv(1024)

                for user in users:
                    if user.onlineStatus == 1 and user != currentUser:
                        user.newMessages.append([currentUser.username, messageToSend])
                message = 'Broadcast sent successfully!\n-o'
                conn.send(message)
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
            elif (data[:1] == '5'):
                #See friends
                if len(currentUser.friends) == 0:
                    message = 'You have 0 friends.\n-o'
                else:
                    #User has friends in the friends list
                    message = currentUser.printFriends()
                conn.send(message)
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
            elif (data[:1] == '6'):
                #Send friend request
                foundFriend = 0

                message = 'Please enter a user to add: -m'
                conn.send(message)
                friend = conn.recv(1024)
                for item in users:
                    if item.username == friend:
                        try:
                            item.friends.index(currentUser)
                            foundFriend = 2
                        except ValueError:
                            foundFriend = 1
                            item.friendRequests.append(currentUser)
                            foundFriend = 1
                if foundFriend == 1:
                    #Added friend 
                    message = 'Friend request sent to ' + friend + ' successfully.\n-o'
                elif foundFriend == 2:
                    #Already friends
                    message = 'Already friends with ' + friend + '\n-o'
                else:
                    message = 'ERROR: Could not find user: ' + friend + '\n-o'
                conn.send(message)
                ack = conn.recv(1024)
                if ack != 'ACK':
                    ackError(conn, currentUser)
            elif (data[:1] == '7'):
                #Friend request response
                if len(currentUser.friendRequests) == 0:
                    #User has 0 friend requests
                    message = 'You have 0 friend requests awaiting response.\n-o'
                    conn.send(message)
                    ack = conn.recv(1024)
                    if ack != 'ACK':
                        ackError(conn, currentUser)
                else:
                    #User has awaiting friend requests
                    for request in currentUser.friendRequests:
                        message = request.username + ' wants to be your friend\n'
                        message += 'Accept (A) or Deny (D): -m'
                        conn.send(message)
                        reply = conn.recv(1024)
                        if reply.lower() == 'accept' or reply.lower() == 'a':
                            #Add friend to current friends list
                            currentUser.friends.append(request)
                            #Add current to requester friends list
                            request.friends.append(currentUser)
                            message = 'Accepted ' + request.username + '\'s friend request!\n-o'
                            conn.send(message)
                            ack = conn.recv(1024)
                            if ack != 'ACK':
                                ackError(conn, currentUser)
                        else:
                            #Do not add friend
                            message = 'Denied ' + request.username + '\'s friend request.\n-o'
                            conn.send(message)
                            ack = conn.recv(1024)
                            if ack != 'ACK':
                                ackError(conn, currentUser)
                    currentUser.friendRequests = []
            
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