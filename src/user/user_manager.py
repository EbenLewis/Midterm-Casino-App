import json
import bcrypt


def load_users():
    with open("data/user.json", "r") as file:
        return json.load(file)


def save_users(users):
    with open("data/user.json", "w") as file:
        json.dump(users, file, indent=4)


class UserManager:
    @classmethod
    def new_user(cls, username: str, password: str, initial_balance: float) -> dict:
        users = load_users() 

        # check for duplicate username
        for user in users:
            if user["username"].lower() == username.lower():
                return {"success": False, "message": "Username already exists"}

        # hash password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = {
            "username": username,
            "password": hashed_password.decode("utf-8"),
            "userid": len(users) + 1,
            "money_total": initial_balance,
            "money_won": 0.0,
            "money_lost": 0.0,
        }

        users.append(new_user)
        save_users(users)
        return {"success": True, "user": new_user}

    @classmethod
    def login(cls, username: str, password: str) -> bool:
        users = load_users()

        for user in users:
            if user["username"].lower() == username.lower():
                return bcrypt.checkpw(
                    password.encode("utf-8"), user["password"].encode("utf-8")
                )
        return False

    @classmethod
    def view_data(cls, username: str) -> dict:
        users = load_users()

        for user in users:
            if user["username"].lower() == username.lower():
                return user
        return {}


class User:
    def __init__(self, username: str):
        self.username = username
        self.data = UserManager.view_data(username)

    def add_funds(self, amount: float):
        users = load_users()

        for user in users:
            if user["username"].lower() == self.username.lower():
                user["money_total"] += amount
                save_users(users)
                self.data = user
                return

    def update_money_won(self, amount: float):
        users = load_users()

        for user in users:
            if user["username"].lower() == self.username.lower():
                user["money_total"] += amount
                user["money_won"] += amount
                save_users(users)
                self.data = user
                return

    def update_money_lost(self, amount: float):
        users = load_users()

        for user in users:
            if user["username"].lower() == self.username.lower():
                user["money_total"] -= amount
                user["money_lost"] += amount
                save_users(users)
                self.data = user
                return

    def remove_funds(self, amount: float):
        users = load_users()

        for user in users:
            if user["username"].lower() == self.username.lower():
                user["money_total"] -= amount
                save_users(users)
                self.data = user
                return
