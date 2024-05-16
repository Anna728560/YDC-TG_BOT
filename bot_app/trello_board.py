import os

import requests
from dotenv import load_dotenv


load_dotenv()

TRELLO_APY_KEY = os.getenv("TRELLO_APY_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")


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
    board_id = create_board()
    list_names = ["Done", "InProgress"]
    for name in list_names:
        create_list(board_id, name)
    print(f"Created board with id {board_id}; "
          f"columns: {', '.join(list_names)}")


if __name__ == "__main__":
    setup_trello_board()
