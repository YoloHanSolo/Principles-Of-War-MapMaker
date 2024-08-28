from requests import put, post
from sys import exit
from os import listdir
from pwinput import pwinput


SERVER_URL = "127.0.0.1:5000"

if __name__ == "__main__":

    email = input("email: ")
    password = pwinput("password: ", "*")

    response = None
    try:
        print("INFO: authenticating...")
        response = post(
            url=f"http://{SERVER_URL}/users/signin",
            json={
                "email": email,
                "password": password
            })

        if response.status_code == 200:
            print("INFO: authenticated")
        elif response.status_code == 400:
            print("ERROR: web server response 400")
            exit()
        elif response.status_code == 401:
            print("ERROR: invalid credentials 401")
            exit()
        elif response.status_code == 404:
            print("ERROR: web server response 404")
            exit()
    except:
        print("ERROR: server offline")
        exit()

    map_id = input("Enter map_id: ")
    map_filename = map_id + ".json"
    if map_filename not in listdir("../maps"):
        print(f"ERROR: invalid map id '{map_id}'")
        exit()

    try:
        with open(f"../maps/{map_filename}", "rb") as file:
            response = put(
                url=f"http://{SERVER_URL}/maps/upload",
                data=file,
                headers={
                    "Authorization": f"Bearer {response.json()['jwt_token']}",
                    "Content-Type": "application/json"
                })
            
            if response.status_code == 200:
                print(f"INFO: success 200")
            elif response.status_code == 400:
                print("ERROR: web server response 400")
                exit()
            elif response.status_code == 401:
                print("ERROR: invalid credentials 401")
                exit()
            elif response.status_code == 415:
                print("ERROR: unsupported media type 415")
                exit()
    except:
        print(f"ERROR: could not open file '../maps/{map_filename}'")
        exit()        

    exit()  