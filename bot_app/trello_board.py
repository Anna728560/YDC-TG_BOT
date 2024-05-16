import os

import requests
from dotenv import load_dotenv


load_dotenv()

TRELLO_APY_KEY = os.getenv("TRELLO_APY_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")


def check_board_exists() -> bool:
    url = "https://api.trello.com/1/members/me/boards"
    query = {
        "key": TRELLO_APY_KEY,
        "token": TRELLO_TOKEN,
    }
    response = requests.get(url, params=query)
    boards = response.json()
    for board in boards:
        if board["name"] == "Trello_Tg_Bot_Board":
            return True
    return False


def create_board():
    url = "https://api.trello.com/1/boards/"
    query = {
        "key": TRELLO_APY_KEY,
        "token": TRELLO_TOKEN,
        "name": "Trello_Tg_Bot_Board",
        "defaultLists": "false"
    }
    response = requests.post(url, params=query)
    board_id = response.json()["id"]
    return board_id


def create_list(board_id, list_name):
    url = f"https://api.trello.com/1/lists"
    query = {
        "key": TRELLO_APY_KEY,
        "token": TRELLO_TOKEN,
        "name": list_name,
        "idBoard": board_id
    }
    response = requests.post(url, params=query)
    return response.json()["id"]


def setup_trello_board():
    if not check_board_exists():
        board_id = create_board()
        list_names = ["Done", "InProgress"]
        for name in list_names:
            create_list(board_id, name)
        print(f"Created board with id {board_id}; "
              f"columns: {', '.join(list_names)}")
    else:
        print("Board already exists, skipping creation.")


if __name__ == "__main__":
    setup_trello_board()
