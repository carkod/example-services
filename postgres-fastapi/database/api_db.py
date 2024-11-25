import logging
import os
from sqlalchemy import text

from database.user_table import UserTable
from sqlmodel import Session, SQLModel, select, create_engine

# This allows testing/Github action dummy envs
db_url = f'postgresql://{os.getenv("POSTGRES_USER", "postgres")}:{os.getenv("POSTGRES_PASSWORD", "postgres")}@{os.getenv("POSTGRES_HOSTNAME", "localhost")}/{os.getenv("POSTGRES_DB", "postgres")}'
engine = create_engine(
    url=db_url,
)


class ApiDb:
    def __init__(self):
        self.engine = create_engine(
            url=db_url,
        )
        self.session = Session(engine)
        pass

    def init_db(self):
        self.init_users()
        self.session.close()
        logging.info("Finishing db operations")

    def drop_db(self):
        SQLModel.metadata.drop_all(engine)

    def init_users(self):
        """
        Dummy data for testing users table
        """
        # username = os.getenv("USER", "admin")
        # email = os.getenv("EMAIL", "admin@example.com")
        # password = os.getenv("PASSWORD", "admin")

        create_table_query = text("""
            CREATE TABLE IF NOT EXISTS binbot_user (
                id UUID PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                is_active BOOLEAN NOT NULL,
                role VARCHAR(50) NOT NULL,
                full_name VARCHAR(255),
                password VARCHAR(40) NOT NULL,
                username VARCHAR(50) UNIQUE
            )
        """)
        self.session.execute(create_table_query)
        self.session.commit()

        # statement = select(UserTable).where(UserTable.username == username)
        # results = self.session.exec(statement)
        # if results.first():
        #     return

        # user_data = UserTable(
        #     username=username, password=password, email=email, role="admin"
        # )

        # self.session.add(user_data)
        # self.session.commit()

        # Insert additional dummy data
        dummy_users = [
            {
                "id": "uuid-1",
                "email": "user1@example.com",
                "is_active": True,
                "role": "user",
                "full_name": "User One",
                "password": "password1",
                "username": "userone"
            },
            {
                "id": "uuid-2",
                "email": "user2@example.com",
                "is_active": True,
                "role": "user",
                "full_name": "User Two",
                "password": "password2",
                "username": "usertwo"
            }
        ]

        for user in dummy_users:
            user_data = UserTable(**user)
            self.session.add(user_data)

        self.session.commit()
