import requests
import json
import pwinput


class UserError(Exception):
    pass


def register(username, password):
    header_login = {'Content-type': 'application/json'}
    credentials = {'username': username, 'password': password}
    response = requests.post('http://localhost:8000/register/', data=json.dumps(credentials), headers=header_login)
    try:
        response.raise_for_status()
        return f"User {username} created succesfully."
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)


def login(username, password):
    header_login = {'Content-type': 'application/json'}
    credentials = {'username': username, 'password': password}
    response = requests.post('http://localhost:8000/login/', data=json.dumps(credentials), headers=header_login)
    try:
        response.raise_for_status()
        return response.json()['token']
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)


def send_message(auth_token, username_dest, message):
    header_message = {'Content-type': 'application/json', 'Authorization': f'Token {auth_token}'}
    message_request = {'username': username_dest, 'message': message}
    response = requests.post('http://localhost:8000/send-message/', data=json.dumps(message_request), headers=header_message)
    try:
        response.raise_for_status()
        response_json = json.loads(response.text)
        if 'UserError' in response_json:
            raise UserError(response_json['UserError'])
        return f"Message to {username_dest} was sent succesfully."
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    except UserError as e:
        return "Error: " + str(e)


def get_messages(auth_token):
    header_message = {'Content-type': 'application/json', 'Authorization': f'Token {auth_token}'}
    response = requests.get('http://localhost:8000/get-messages/', headers=header_message)
    try:
        response.raise_for_status()
        message_list = json.loads(response.text)
        for message in message_list:
            print(f"{message['timestamp']} {message['source']} --> {message['destination']}: {message['message']}")
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)


print("Chat App")
print("Choose options:")
print("1. Login")
print("2. Register")
print("3. Send message")
print("4. View received messages")
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
        if auth_token.startswith("Error"):
            print(auth_token)
        else:
            print(f"You are now logged in as {username}.")
    elif option == ord('2'):
        print("Register your account")
        username = input("Enter username: ")
        password = pwinput.pwinput(prompt='Enter password: ', mask='*')
        print(register(username, password))
    elif option == ord('3'):
        print("Send message:")
        if auth_token == "" or auth_token.startswith("Error"):
            print("You are not logged in. Please log into your account.")
        else:
            username_dest = input("Enter user to which you will send the message: ")
            message = input("Enter message to send: ")
            print(send_message(auth_token=auth_token, username_dest=username_dest, message=message))
    elif option == ord('4'):
        if auth_token == "" or auth_token.startswith("Error"):
            print("You are not logged in. Please log into your account to see received messages.")
        else:
            print("Messages sent to current user:")
            get_messages(auth_token)
    elif option == ord('q'):
        print("Exiting Chat App...")
