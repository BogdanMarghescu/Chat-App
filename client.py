import requests
import json
import pwinput


def register(username, password):
    header_login = {'Content-type': 'application/json'}
    credentials = {'username': username, 'password': password}
    response = requests.post('http://localhost:8000/register/', data=json.dumps(credentials), headers=header_login)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    print(f"User {username} created succesfully.")


def login(username, password):
    header_login = {'Content-type': 'application/json'}
    credentials = {'username': username, 'password': password}
    response = requests.post('http://localhost:8000/login/', data=json.dumps(credentials), headers=header_login)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    auth_token = response.json()['token']
    return auth_token


def send_message(auth_token, username_dest, message):
    header_message = {'Content-type': 'application/json', 'Authorization': f'Token {auth_token}'}
    message_request = {'username': username_dest, 'message': message}
    response = requests.post('http://localhost:8000/send-message/', data=json.dumps(message_request), headers=header_message)
    try:
        response.raise_for_status()
        print(f"Message to {username_dest} was sent succesfully.")
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)


print("Chat App")
print("Choose options:")
print("1. Login")
print("2. Register")
print("3. Send Message")
print("q. Exit")
option = 0
auth_token = ''
while option != ord('q'):
    option = ord(input("\nInsert option: "))
    if option == ord('1'):
        print("Log into your account")
        username = input("Enter username: ")
        password = pwinput.pwinput(prompt='Enter password: ', mask='*')
        auth_token = login(username, password)
        print(f"You are now logged in as {username}.")
        print(auth_token)
    elif option == ord('2'):
        print("Register your account")
        username = input("Enter username: ")
        password = pwinput.pwinput(prompt='Enter password: ', mask='*')
        register(username, password)
    elif option == ord('3'):
        print("Send message:")
        if auth_token == "":
            print("You are not logged in. Please log into your account.")
        else:
            username_dest = input("Enter user to which you will send the message: ")
            message = input("Enter message to send: ")
            send_message(auth_token=auth_token, username_dest=username_dest, message=message)
    elif option == ord('q'):
        print("Exiting Chat App...")
