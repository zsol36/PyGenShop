from schemas.schema import User, Basket, Item, UpdateItem
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json, update_item, delete_item, read_json_file, write_json_file
from data.filereader import get_user_by_id, get_basket_by_user_id, get_all_users, get_total_price_of_basket, load_json

routers = APIRouter()

@routers.post('/adduser',response_model=User)
def adduser(user : User):
    new_user = user.model_dump()
    try:
        add_user(new_user)
        return JSONResponse(content=new_user,status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except:
        raise HTTPException(status_code=418,detail="unkown error has occured")

@routers.post('/addshoppingbag',response_model=str)
def addshoppingbag(userid: int) -> str:
    data = load_json()    
    new_basket = {
        "id" : max([u["id"] for u in data["Baskets"]],default = 0) + 1,
        "user_id" : userid,
        "items": []
    }
    try:
        add_basket(new_basket)
        return JSONResponse(content="sikeres kosár hozzárendelés",status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    except:
        raise HTTPException(status_code=418,detail="unkown error has occured")

@routers.post('/additem',response_model=list[Item])
def additem(userid: int, item : Item):
    mitem = item.model_dump()
    try:
        add_item_to_basket(userid,mitem)
        return get_basket_by_user_id(userid)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except:
        raise HTTPException(status_code=418,detail="unkown error has occured")
@routers.put('/updateitem',response_model=list[Item])
def updateitem(userid: int, itemid: int, updateItem : UpdateItem):
    try:
        update_item(userid,itemid,updateItem.model_dump(exclude_none=True))
        return get_basket_by_user_id(userid)
    except ValueError as e:    
         raise HTTPException(status_code=404, detail=str(e))
    except:
        raise HTTPException(status_code=418,detail="unkown error has occured")

@routers.delete('/deleteitem',response_model=list[Item])
def deleteitem(userid: int, itemid: int):
    try:
        delete_item(userid,itemid)
        return get_basket_by_user_id(userid)
    except ValueError as e:
         raise HTTPException(status_code=404, detail=str(e))
    except:
        raise HTTPException(status_code=418,detail="unkown error has occured")

@routers.get('/user',response_model=User)
def user(userid: int):
   try:
        return JSONResponse(content=get_user_by_id(userid),status_code=200)
   except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

@routers.get('/users',response_model=list[User])
def users():
    users = get_all_users()
    return JSONResponse(content=users, status_code=200)

@routers.get('/shoppingbag',response_model=list[Item])
def shoppingbag(userid: int):
    try:

        return JSONResponse(content=get_basket_by_user_id(userid),status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

@routers.get('/getusertotal',response_model=list[User])
def getusertotal(userid: int) -> float:
    try:
        return JSONResponse(content=get_total_price_of_basket(userid),status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
        

@routers.post("/save")
def save(source: str, dest: str):
    try:
        data = read_json_file(source)
        write_json_file(dest, data)
        return JSONResponse(status_code=201,content="sucessfull save")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Source file not found")
    except Exception:
        raise HTTPException(status_code=418, detail="unkown error has occured")
    
@routers.post("/reload")
def reload(dest: str, source: str):
    try:
        data = read_json_file(dest)
        write_json_file(source, data)
        return JSONResponse(status_code=200,content="sucessfull reload")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Source file not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Unknown error")