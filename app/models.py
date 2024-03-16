
#Python3 객체와 DB table을 연결하는 정보
#CREATE TABLE에 직접적인 역할을 수행 (PRIMARY KEY, FOREIGN KEY, INDEX etc...)


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# User 클래스와 DB의 users 테이블을 연결
class User(Base):
	__tablename__ = 'users'
	
	# attributes
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(length=128), unique=True, index=True)
	salt = Column(String(length=128))
	password = Column(String(length=128))
	pastes = relationship('Paste', back_populates='owner')

# Paste 클래스와 DB의 pastes 테이블을 연결
class Paste(Base):
	__tablename__ = 'pastes'

	# attributes
	id = Column(Integer, primary_key=True, index=True)
	# Need some attributes more
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship('User', back_populates='pastes')
	
	title = Column(String(length=128))
	content = Column('content', String(length=1000))
	


