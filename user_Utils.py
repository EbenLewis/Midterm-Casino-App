import json
import bcrypt


def load_users():
    with open("user.json", "r") as file:
        return json.load(file)


def save_users(users):
    with open("user.json", "w") as file:
        json.dump(users, file, indent=4)


class UserManager:
    @classmethod
    def new_user(cls, username: str, password: str, initial_balance: float) -> dict:
        users = load_users()

        # check for duplicate username
        for user in users:
            if user["username"] == username:
                return {"success": False, "message": "Username already exists"}

        # hash password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = {
            "username": username,
            "password": hashed_password.decode("utf-8"),
            "userid": len(users) + 1,
            "money_total": initial_balance,
        }

        users.append(new_user)
        save_users(users)
        return {"success": True, "user": new_user}

    @classmethod
    def login(cls, username: str, password: str) -> bool:
        users = load_users()

        for user in users:
            if user["username"] == username:
                return bcrypt.checkpw(
                    password.encode("utf-8"), user["password"].encode("utf-8")
                )
        return False

    @classmethod
    def view_data(cls, username: str) -> dict:
        users = load_users()

        for user in users:
            if user["username"] == username:
                return user
        return {}

