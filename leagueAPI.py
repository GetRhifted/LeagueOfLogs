from fastapi import Body, Path, Query, Depends, FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import Field, BaseModel
from typing import List, Optional
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer



point = FastAPI()
point.title = 'ChampStats'
point.version = 'Alpha 0.1'

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'megustaellol@gamil.com':
            raise HTTPException(status_code=403, detail='Credenciales Invalidas.')

class User(BaseModel):
    email: str
    password: str        

class Champ(BaseModel):
    id : Optional[int] = None
    name : str = Field(min_length=1, max_length=15)
    role : str = Field(min_length=3, max_length=15)
    win_rate : float = Field(ge=1, le=100)
    ban_rate : float = Field(ge=1, le=100)
    tier : int = Field(le=10)

    class Cofing:
        schema_extra ={
            'example' : {
                'id' : 1,
                'name' : 'Nombre del Campeon.',
                'role' : 'Rol(es) del Campeon.',
                'win_rate' : 'Porcentaje de Victorias.',
                'ban_rate' : 'Porcentaje de Baneos.',
                'tier' : 'Tier del personaje.'
            }
        }

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

@point.post('/Login', tags=['Auth'])
def login(user: User):
    if user.email == 'megustaellol@gamil.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@point.get('/Champs/{id}', tags=['Champs'], status_code=200)
def get_champs(id: int = Path(ge=1, le=500)):
    message = 'Este no es un id de campeon valido, intentalo de nuevo.'
    for champ in champions:
        if champ['id'] == id:
            return JSONResponse(status_code=200, content=champ)
    return JSONResponse(status_code=404, content=message)

@point.get('/Champs/', tags=['Champs'])
def get_champs_by_role(role: str = Query(min_length=3, max_length=15)):
    results = []
    for champ in champions:
        roles = champ['role'].split(',')
        if role in roles:
            results.append(champ)
        else:
            for rol in roles:
                if role == rol.strip():
                    results.append(champ)
                    break
    return JSONResponse(status_code=200, content=results)

@point.post('/Champs', tags=['Champs'], status_code=201, dependencies=[Depends(JWTBearer())])
def upload_champ(champ: Champ):
    champions.append(champ)
    return JSONResponse(status_code=201, content={'message': 'El campeon ha sido añadido a la base de datos!'})

@point.put('/Champs/{id}', tags=['Champs'], status_code=200, dependencies=[Depends(JWTBearer())])
def update_champ(id: int, champ: Champ):
    for item in champions:
        if item['id'] == id:
            item['name'] = champ.name
            item['role'] = champ.role
            item['win_rate'] = champ.win_rate
            item['ban_rate'] = champ.ban_rate
            item['tier'] = champ.tier
            return JSONResponse(status_code=200, content={'message': 'Se ha actualizado el campeon en la base de datos!'})
        else:
            return JSONResponse(status_code=404, content={'message': 'El id indicado no existe en nuestra base de datos, intetelo de nuevo.' })

@point.delete('/Champs', tags=['Champs'], status_code=200, dependencies=[Depends(JWTBearer())])
def delete_champ(id: int, champ: Champ):
    for item in champions:
        if item['id'] == id:
            champions.remove(item)
            return JSONResponse(status_code=200, content={'message': 'El campeon ha sido eliminado de la base de datos!'})
        else:
            return JSONResponse(status_code=404, content={'message': 'El id indicado no existe en nuestra base de datos, intetelo de nuevo.'})
        