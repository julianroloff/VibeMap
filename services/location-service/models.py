from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from dependencies import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    stress_level = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    geom = Column(Geometry("POINT"), nullable=False)  # PostGIS for spatial data