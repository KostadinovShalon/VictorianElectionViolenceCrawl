from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker()
Base = declarative_base()


def change_session_data(user, password, host):
    engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/evp?charset=latin1')
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)
