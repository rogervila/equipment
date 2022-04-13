from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import declarative_base


class Product(declarative_base()):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Integer, default=0, nullable=False)
