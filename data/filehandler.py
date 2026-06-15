import json
import os
from typing import Dict, Any

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    with open(JSON_FILE_PATH,"r", encoding="utf-8") as file:
        return json.load(file)

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data,file,indent=2,ensure_ascii=False)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    for i in data["Users"]:
        if user["id"] == i["id"]:
            raise ValueError("id already exists, chose a different id")
        if user["email"] == i["email"]:
            raise ValueError("user with same email exits")
    data["Users"].append(user)
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    for i in data["Baskets"]:
        if i["user_id"] == basket["user_id"]:
            raise ValueError("You already have a basket")
   
    for i in data["Users"]:
        if i["id"] == basket["user_id"]:
            data["Baskets"].append(basket)
            save_json(data)
            return
    raise ValueError("User not found")

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    data = load_json()
    founduser = False
    for i in data["Baskets"]:
        if i["user_id"] == user_id:
            i["items"].append(item)
            founduser = True
            break
    save_json(data)
    if not founduser:
        raise ValueError("Error couldn't find your basket. Maybe you don't have one yet?")
    
def update_item(user_id: int, itemid : int, newitem: Dict[str,Any]) -> None:
    data = load_json()
    isfound = False
    for i in data["Baskets"]:
        if i["user_id"] == user_id:
            isfound = True
            for y in i["items"]:
                if y["item_id"] == itemid:
                    isfound = isfound and True
                    for key, value in newitem.items():
                        y[key] = value

                    save_json(data)

    if not isfound:                
        raise ValueError("Item or Basket not found")
                
def delete_item(user_id:int,itemid:int) -> None:
    data = load_json()
    isfound = False
    for i in data["Baskets"]:
        if i["user_id"] == user_id:
            isfound = True
            for y in i["items"]:
                if y["item_id"] == itemid:
                    isfound = isfound and True
                    i["items"].remove(y)
                    save_json(data)
    if not isfound:                
        raise ValueError("Item or Basket not found")
    

def read_json_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_file(path: str, data: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)