from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from .config import settings





SQLALCHEMY_DATABASE_URL =  f'postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




        

# # THIS IS FOR THE RECORD NOT BEING USED

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time



# while True:

#     try:
#         conn = psycopg2.connect(host = 'localhost', 
#                            database='fastapi', 
#                            user='postgres', 
#                            password='Cheddar2023!!', 
#                            cursor_factory=RealDictCursor )
#         cursor = conn.cursor()
#         print("Database connection was successfull")
#         break

#     except Exception as error:
#         print ("Connection failed")
#         print("Error: " , error)
#         time.sleep(2)
