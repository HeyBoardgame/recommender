from sqlalchemy import Column, BigInteger

from src.database import Base


class User(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True, index=True)
    user_index = Column(BigInteger)
