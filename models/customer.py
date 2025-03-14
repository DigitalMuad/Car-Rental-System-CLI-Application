from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)

    # Relationships

    rentals = relationship("Rental", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name} ({self.email})>"