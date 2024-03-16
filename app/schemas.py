"""

Python3 데이터형식 검증(pydantic)
데이터를 읽거나 쓸 때 객체 멤버 변수의 타입을 체크
(테이블과 일관성 유지)
"""

from typing import List, Union
from pydantic import BaseModel

class PasteBase(BaseModel):
	title: str

class PasteCreate(PasteBase):
	content: str
	
class Paste(PasteCreate):
	id: int
	class Config:
		orm_mode = True	
class PasteDetail(Paste):
	owner_id: int	

class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str

class User(UserBase):
	id: int
	pastes: List[Paste] = []
	
	class Config:
		orm_mode = True
	
class UserDetail(User):
	salt: str
