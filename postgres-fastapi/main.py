from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging
import os
from uuid import uuid4
from sqlalchemy import text, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from fastapi.routing import APIRoute

# This allows testing/Github action dummy envs
db_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="postgres",
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database="postgres",
    port=os.getenv("POSTGRES_PORT", 5432),
)
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def database_ops():
    session = SessionLocal()
    try:
        # Create table if not exists
        create_table_query = text("""
            CREATE TABLE IF NOT EXISTS binbot_user (
                id VARCHAR(255) PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                is_active BOOLEAN NOT NULL,
                role VARCHAR(50) NOT NULL,
                full_name VARCHAR(255),
                password VARCHAR(40) NOT NULL,
                username VARCHAR(50) NOT NULL
            )
        """)
        session.execute(create_table_query)
        session.commit()
        print("Table created or already exists")

        # Insert a single user
        insert_user_query = text("""
            INSERT INTO binbot_user (id, email, is_active, role, full_name, password, username)
            VALUES (:id, :email, :is_active, :role, :full_name, :password, :username)
        """)
        user = {
            "id": uuid4().hex,
            "email": "user@example.com",
            "is_active": True,
            "role": "admin",
            "full_name": "John Doe",
            "password": "securepassword",
            "username": "johndoe",
        }
        session.execute(insert_user_query, user)
        session.commit()
        print("User inserted successfully")
    finally:
        print("Closing session")
        session.close()

database_ops()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# if __name__ == "__main__":
#     app()