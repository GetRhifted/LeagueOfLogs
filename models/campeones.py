from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Campeones(Base):

    __tablename__= 'champions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)
    win_rate = Column(Float)
    ban_rate = Column(Float)
    tier = Column(Integer)