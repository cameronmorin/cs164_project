class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.unreadMessages = []    #[[sender.username, message]]
        self.newMessages = []       #Used for real-time messages
        self.timeline = []
        self.friends = []
        self.friendRequests = []
        self.onlineStatus = 0       #Default to offline
        self.connection = 0         #Defalut empty connection

    def changePassword(self, newPassword):
        self.password = newPassword
    