import json


class Database:
    def __init__(self):
        self.users = []
        database_path = r"D:\Git\proiectrcp2023-echipa-4-2023\package.json"

        with open(database_path, 'r') as file:
            data = json.load(file)

        credentials = data.get('credentials', [])

        for user in credentials:
            username = user.get('username')
            password = user.get('password')
            self.users.append((username, password))

    def check_user(self, username, password):
        if (username, password) in self.users:
            return True
        return False
