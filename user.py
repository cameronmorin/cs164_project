class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.unreadMessages = []    #[[sender.username, message]]
        self.newMessages = []       #Used for real-time messages
        self.timeline = []
        self.friends = []
        self.friendRequests = []    #[User object]
        self.onlineStatus = 0       #Default to offline
        self.connection = 0         #Defalut empty connection

    def changePassword(self, newPassword):
        self.password = newPassword
    
    def printFriends(self):
        num = 1
        toSend = 'Your Friends:\n'
        for friend in self.friends:
            toSend += str(num) + ': ' + friend.username + '   Status: '
            if friend.onlineStatus == 0:
                #Offline
                toSend += 'Offline\n'
            else:
                toSend += 'Online\n'
        toSend += '-o'
        return toSend