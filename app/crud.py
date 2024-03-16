"""
데이터핸들링 관련 함수
직접 데이터베이스 세션에 접근 (DB 세션은 database.py에서 담당)
함수 인자로 사용자가 보낸 각종 파라미터를 받아서 처리(CRUD)
"""

import hashlib
import secrets

from sqlalchemy.orm import Session
# models.py, schemas.py와 같은 디렉터리에 위치
from . import models, schemas

def get_pastes_by_username(db: Session, username: str, skip: int = 0, limit: int = 100):
	user_id = db.query(models.User).with_entities(models.User.id,).filter(models.User.username == username).first()[0]
	return db.query(models.Paste).filter(models.Paste.owner_id == user_id).order_by(models.Paste.id.asc()).all()

def create_paste(db: Session, paste: schemas.PasteCreate, owner_id: int):
	new_paste = models.Paste(owner_id=owner_id, title=paste.title, content=paste.content)
	db.add(new_paste)
	db.commit()
	db.refresh(new_paste)
	
	return new_paste;

def get_user(db: Session, username: str):
	return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_username(db: Session, username: str):
	return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
	return db.query(models.User).order_by(models.User.id.asc()).offset(skip).limit(limit).all()



def create_user(db: Session, user: schemas.UserCreate):
	# plain password + salt = Hashed password -> DB 저장
	m = hashlib.sha256()
	salt = secrets.token_bytes(16).hex()
	m.update(user.password.encode('utf-8'))
	m.update(bytes.fromhex(salt))
	password = m.hexdigest()

	# db에 새로운 유저 정보 추가
	db_user = models.User(username=user.username, salt=salt, password=password)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)

	return db_user

	
def verify_user(db: Session, username: str, password: str):
	# model.User -> users 테이블에서 username은 유니크 (최대 한개의 데이터)
	db_user = db.query(models.User).filter(models.User.username == username).first()
	# username이 존재하지 않음
	if db_user is None:
		return None
	# password 복호화
	m = hashlib.sha256()
	m.update(password.encode('utf-8'))
	m.update(bytes.fromhex(db_user.salt))
	password = m.hexdigest()
	# DB의 사용자 비밀번호와 파라미터로 받은 password가 일치X -> 인증실패
	if db_user.password != password:
		return None

	return db_user












