from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.campeones import Campeones
from fastapi.encoders import jsonable_encoder
from services.campeones import ChampionService
from schemas.champion import Champ
from middlewares.jwt_bearer import JWTBearer


champion_router = APIRouter()

@champion_router.get('/Champs/{id}', tags=['Champs'], status_code=200)
def get_champs(id: int = Path(ge=1, le=500)):
    message = 'Este no es un id de campeon valido, intentalo de nuevo.'
    db = Session()
    result = ChampionService(db).get_champ(id)
    if not result:
        return JSONResponse(status_code=404, content=message)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
   
@champion_router.get('/Champs/', tags=['Champs'])
def get_champs_by_role(role: str = Query(min_length=3, max_length=15)):
    db = Session()
    result = ChampionService(db).get_champ_by_role(role)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Parece que ingresaste un rol invalido, prueba de nuevo.'})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@champion_router.post('/Champs', tags=['Champs'], status_code=201, dependencies=[Depends(JWTBearer())])
def upload_champ(champ: Champ):
    db = Session()
    ChampionService(db).upload_champ(champ)
    return JSONResponse(status_code=201, content={'message': 'El campeon ha sido añadido a la base de datos!'})

@champion_router.put('/Champs/{id}', tags=['Champs'], status_code=200, dependencies=[Depends(JWTBearer())])
def update_champ(id: int, champ: Champ):
    db = Session()
    result = ChampionService(db).get_champ(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'El id indicado no existe en nuestra base de datos, intetelo de nuevo.' })
    ChampionService(db).update_champ(id, champ)
    db.commit
    return JSONResponse(status_code=200, content={'message': 'Se ha actualizado el campeon en la base de datos!'})

@champion_router.delete('/Champs', tags=['Champs'], status_code=200, dependencies=[Depends(JWTBearer())])
def delete_champ(id: int, champ: Champ):
    db = Session()
    result = ChampionService(db).get_champ(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'El id indicado no existe en nuestra base de datos, intetelo de nuevo.' })
    ChampionService(db).delete_champ(id)
    return JSONResponse(status_code=200, content={'message': 'El campeon ha sido eliminado de la base de datos!'})
       
        