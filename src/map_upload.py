from requests import put, post
from sys import exit
from json import load, dump
from os import listdir, path, makedirs
from inquirer import Text, Password, List, Confirm, prompt
from src.types.enums import Stage

BASE_DIR = path.dirname(path.abspath(__file__))
ROOT_DIR = path.abspath(path.join(BASE_DIR, ".."))
MAPS_DIR = path.join(ROOT_DIR, "maps")

CACHE_DIR = path.join(ROOT_DIR, ".cache")
TOKEN_FILE = path.join(CACHE_DIR, "jwt_token.json")
makedirs(CACHE_DIR, exist_ok=True)

server_urls = {
    Stage.DEV.value: "http://127.0.0.1:5001",
    Stage.PROD.value: "https://web-server.principles-of-war.com",
}


def get_cached_token(stage):
    if path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = load(f)
            return data.get(stage)
        except Exception:
            pass
    return None


def save_token(stage, jwt_token):
    data = {}
    if path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                data = load(f)
        except Exception:
            pass
    data[stage] = jwt_token
    with open(TOKEN_FILE, "w") as f:
        dump(data, f)


def run():

    values = prompt(
        [
            List(name="filename", message="map", choices=listdir(MAPS_DIR)),
            List(
                name="stage", message="stage", choices=[value.value for value in Stage]
            ),
        ]
    )

    filename = values["filename"]
    stage = values["stage"]
    server_url = server_urls[stage]

    jwt_token = get_cached_token(stage)

    if jwt_token:
        use_cached = prompt(
            [
                Confirm(
                    name="use_cached",
                    message=f"Cached credentials found for '{stage}'. Use them?",
                    default=True,
                )
            ]
        )["use_cached"]

        if use_cached:
            print("[INFO] Using cached JWT token")
        else:
            jwt_token = None

    if not jwt_token:
        credentials = prompt(
            [
                Text(name="email", message="email"),
                Password(name="password", message="password"),
            ]
        )
        email = credentials["email"]
        password = credentials["password"]

        response = None
        try:
            print(f"[INFO] POST {server_url}/users/signin")
            response = post(
                url=f"{server_url}/users/signin",
                json={"email": email, "password": password},
            )

            if response.status_code == 200:
                print("[INFO] authenticated")
                jwt_token = response.json()["jwt_token"]
                save_token(stage, jwt_token)
            elif response.status_code == 400:
                print("[ERROR] web server response 400")
                exit()
            elif response.status_code == 401:
                print("[ERROR] invalid credentials 401")
                exit()
            elif response.status_code == 404:
                print("[ERROR] web server response 404")
                exit()
        except:
            print("[ERROR] server offline")
            exit()

    if filename not in listdir(MAPS_DIR):
        print(f"[ERROR] invalid filename '{filename}'")
        exit()

    try:
        with open(f"{MAPS_DIR}/{filename}", "rb") as file:
            print(f"[INFO] PUT {server_url}/maps/upload")
            response = put(
                url=f"{server_url}/maps/upload",
                data=file,
                headers={
                    "Authorization": f"Bearer {jwt_token}",
                    "Content-Type": "application/json",
                },
            )

            if response.status_code == 200:
                print(f"[INFO] success 200 - {response.json()['status']}")
            elif response.status_code == 400:
                print("[ERROR] web server response 400")
                exit()
            elif response.status_code == 401:
                print("[ERROR] invalid credentials 401")
                exit()
            elif response.status_code == 415:
                print("[ERROR] unsupported media type 415")
                exit()
    except FileNotFoundError:
        print(f"[ERROR] could not open file '{MAPS_DIR}/{filename}'")
        exit()
    except Exception as e:
        print(f"[ERROR] upload failed: {e}")
        exit()

    exit()
