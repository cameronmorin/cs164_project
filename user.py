class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.unreadMessages = []
        self.timeline = []
        self.friends = []
        self.friendRequests = []

    def changePassword(self, newPassword):
        self.password = newPassword
    