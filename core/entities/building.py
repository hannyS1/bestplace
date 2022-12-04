from sqlalchemy import Column, Integer, String, Float, DECIMAL

from config.database import Base


class ApartmentBuilding(Base):
    __tablename__ = "apartment_building"

    id = Column(Integer, primary_key=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    apartments_count = Column(Integer, nullable=False)
    price = Column(DECIMAL(precision=1), nullable=False)
    year = Column(Integer, nullable=False)
    h3_value = Column(String, nullable=False, index=True)
