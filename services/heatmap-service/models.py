from sqlalchemy import Column, Integer, Float
from dependencies import Base

class HeatmapData(Base):
    __tablename__ = "heatmap_data"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    aggregated_stress = Column(Float, nullable=False)
    
    # ToDo: Size of Heatmap Bubble
    # ToDo: Opacity
    