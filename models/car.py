from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from database.base import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    daily_rate = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    # Relationships
    rentals = relationship("Rental", back_populates="car")
     
    def __repr__(self):
        return f"<Car {self.make} {self.model} ({self.year})>"