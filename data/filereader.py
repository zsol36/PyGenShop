import json
import os
from typing import Dict, Any, List


JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    with open(JSON_FILE_PATH,"r", encoding="utf-8") as file:
        return json.load(file)

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    data = load_json()
    for i in data["Users"]:
        if i["id"] == user_id:
            return i
    raise ValueError("Can't find user with this userid")
def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    data = load_json()
    for i in data["Baskets"]:
        if i["user_id"] == user_id:
            return i["items"]
    raise ValueError("Can't find basket with this userid")
def get_all_users() -> List[Dict[str, Any]]:
    data = load_json()
    users = data["Users"]
    return users

def get_total_price_of_basket(user_id: int) -> float:
    data = load_json()
    for i in data["Baskets"]:
        if i["user_id"] == user_id:
            return sum(x["price"] * x["quantity"] for x in i["items"])
    raise ValueError("Can't find basket with this userid")        
