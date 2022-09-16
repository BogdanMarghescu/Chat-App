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


print("Chat App")
print("Choose options:")
print("1. Login")
print("2. Register")
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
    elif option == ord('q'):
        print("Exiting Chat App...")
