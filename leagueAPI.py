from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.champion import champion_router
from routers.user import user_router

point = FastAPI()
point.title = 'ChampStats'
point.version = 'Alpha 0.1'

point.add_middleware(ErrorHandler)
point.include_router(user_router)
point.include_router(champion_router)

Base.metadata.create_all(bind=engine)
       
champions = [
    {
        'id' : 1,
        'name' : 'Syndra',
        'role' : 'mid lane',
        'win_rate' : 49.20,
        'ban_rate' : 2.06,
        'tier' : 4
    },
    {
        'id' : 2,
        'name' : 'Taliyah',
        'role' : 'mid lane, jungle',
        'win_rate' : 50.50,
        'ban_rate' : 0.21,
        'tier' : 4 
    },
    {
        'id' : 3,
        'name' : 'Orianna',
        'role' : 'mid lane',
        'win_rate' : 49.62,
        'ban_rate' : 0.13,
        'tier' : 4
    },
    {
        'id' : 4,
        'name' : 'Vex',
        'role' : 'mid lane',
        'win_rate' : 51.32,
        'ban_rate' : 5.19,
        'tier' : 2
    }
]

@point.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Tu Guia de Campeones</h1>')
