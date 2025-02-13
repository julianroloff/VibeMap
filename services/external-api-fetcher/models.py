from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from dependencies import Base

class APILocation(Base):
    __tablename__ = "apilocation_db"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sport = Column(String, nullable=False)  
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geom = Column(Geometry("POINT"), nullable=False)  # PostGIS for spatial data
