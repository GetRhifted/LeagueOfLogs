from models.campeones import Campeones
from schemas.champion import Champ


class ChampionService():

    def __init__(self, db) -> None:
        self.db = db

    def get_champ(self, id):
        result = self.db.query(Campeones).filter(Campeones.id == id).first()
        return result
    
    def get_champ_by_role(self, role):
        result = self.db.query(Campeones).filter(Campeones.role.ilike(f"%{role}%")).all()
        return result
    
    def upload_champ(self, champ: Champ):
        new_champ = Campeones(**champ.dict())
        self.db.add(new_champ)
        self.db.commit()
        return
    
    def update_champ(self, id: int, data: Champ):
        champion = self.db.query(Campeones).filter(Campeones.id == id).first()
        champion.name = data.name
        champion.role = data.role
        champion.win_rate = data.win_rate
        champion.ban_rate = data.ban_rate
        champion.tier = data.tier
        self.db.commit()

    def delete_champ(self, id: int):
        result = self.db.query(Campeones).filter(Campeones.id == id).first()
        self.db.delete(result)
        self.db.commit()
        return
