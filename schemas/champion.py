from pydantic import BaseModel, Field
from typing import Optional, List

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