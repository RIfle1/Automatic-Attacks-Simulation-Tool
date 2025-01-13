class Credential:
    def __init__(self, username, password, success=False):
        self.username = username
        self.password = password
        self.success = success

    def __str__(self):
        return f"Username: {self.username}, Password: {self.password}"