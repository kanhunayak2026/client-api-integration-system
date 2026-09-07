from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:your_password@localhost/onefin"

engine = create_engine(DATABASE_URL)
