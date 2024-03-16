# SQLAlchemy : python3에서 사용하는 orm (Object-Relational Mapping)

# 	프로그래밍 언어의 객체와 데이터베이스의 정보를 매핑
# 데이터베이스 연결 모듈
# 데이터베이스와의 세션을 담당
# declaretive_base()로 Python 데이터베이스 모델 기본 객체 생성

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# mariadb+mariadbconnector://{user name}:{user password}@{host}:{port}/{database name}
SQLALCHEMY_DATABASE_URL = 'mariadb+mariadbconnector://pasteuser:8960@127.0.0.1:3306/pastebin'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

