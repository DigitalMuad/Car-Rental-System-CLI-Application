from sqlalchemy import Column, Integer, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from database.base import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    rental_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=False)
    total_cost = Column(Float, nullable=False)

    # Relationships
    car = relationship("Car", back_populates="rentals")
    customer = relationship("Customer", back_populates="rentals")

    def __repr__(self):
        return f"<Rental {self.car_id} rented by {self.customer_id}>"