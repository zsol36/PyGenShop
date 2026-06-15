from fastapi import FastAPI
from schemas.schema import ShopName
from routers.routes import routers as routes_router



app = FastAPI()
app.include_router(routes_router)

@app.get('/')
def route():
    return {'Wellcome to ': ShopName}    
