from core.db import Base, engine
from sqlalchemy import Column, Integer


class Counter(Base):
    __tablename__ = "counter"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, default=0)


Base.metadata.create_all(bind=engine)
