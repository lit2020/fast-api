"""
FastAPI endpoint 제공 모듈
유저가 보낸 request 파싱 -> crud에 알맞게 전송
schemas (pydantic) 를 활용하여 사용자가
받을 수 있는 응답의 형태를 미리 알 수 있음 (response_model)
"""

from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
	# username을 가진 유저를 db에서 read한다
	db_user = crud.get_user_by_username(db, username=user.username)
	# 해당 유저가 이미 존재한다면 exception : username은 유니크해야함.
	if db_user:
		raise HTTPException(status_code=400, detail='username already registered')
	return crud.create_user(db=db, user=user)

@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	users = crud.get_users(db, skip=skip, limit=limit)
	return users

@app.get('/users/{username}', response_model=schemas.User)
def get_user(username:str, db: Session = Depends(get_db)):
	db_user = crud.get_user(db, username=username)
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')
	return db_user

@app.get('/users/{username}/verify/', response_model=schemas.UserDetail)
def verify_user(username: str, password: str, db: Session = Depends(get_db)):
	db_user = crud.verify_user(db, username=username, password=password)
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')
	return db_user


@app.post('/users/{username}/pastes', response_model=schemas.Paste)
def create_paste(username: str, password: str, paste:schemas.PasteCreate, db: Session = Depends(get_db)):
	db_user = verify_user(username=username, password=password, db=db)
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')
	# type(db_user) : models.User 
	# type(db_user.id) : int
	# print(f"+++++++{0}++++++++", type(db_user.id))
	return crud.create_paste(db, paste, owner_id=db_user.id)	

@app.get('/users/{username}/pastes', response_model=List[schemas.Paste])
def get_pastes(username: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_username(db, username=username)
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')	
	return crud.get_pastes_by_username(db, username=username, skip=skip, limit=limit)
	
 







