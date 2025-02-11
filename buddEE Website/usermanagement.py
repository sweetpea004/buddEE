import json
from werkzeug.security import generate_password_hash, check_password_hash


def load_users():
    # Returns a list of dictionaries by opening users.json
    try:
        with open('users.json') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    return users


def save_users(users_list):
    # Saves the given list of dictionaries to users.json
    with open('users.json', 'w') as f:
        json.dump(users_list, f, indent=4)


def user_exists(username):
    # Returns true if user already exists in users.json
    users = load_users()
    user_exists = False
    for user in users:
        if user['username'] == username:
            user_exists = True

    return user_exists


def add_user(username, id, password):
    # Adds the new user to users.json
    users = load_users()
    new_user = {
        "username": username,
        "id": id,
        "password": generate_password_hash(password)
    }
    users.append(new_user)
    save_users(users)


def login(username, password):
    # Returns true or false depending on valid credentials

    users = load_users()

    # Loop over all users and check for valid login info
    successful_login = False
    for user in users:
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                successful_login = True

    return successful_login


def change_username(target_index, new_username):
    # changes the account details of the user if they differ from their current data

    users_list = load_users()

    users_list[target_index]['username'] = new_username

    # save the users_list to account for changes
    save_users(users_list)

def change_password(target_index, new_password):
    # changes the account details of the user if they differ from their current data

    users_list = load_users()

    users_list[target_index]['password'] = generate_password_hash(new_password)

    # save the users_list to account for changes
    save_users(users_list)


def delete_account(given_id):
    # deletes the user's dict from users.json

    # find the index of the user in the json file
    users_list = load_users()

    for index in range(len(users_list)):
        if users_list[index]['id'] == given_id:
            target_index = index

    # Delete the user from users_list
    del users_list[target_index]

    # save the new users_list
    save_users(users_list)
