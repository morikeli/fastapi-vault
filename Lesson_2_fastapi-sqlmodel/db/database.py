from sqlmodel import SQLModel, create_engine


DB_FILE = 'db.sqlite3'
engine = create_engine(f'sqlite:///{DB_FILE}', echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    # create the tables if this file is run independently, as a script
    create_tables()