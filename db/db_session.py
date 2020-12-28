from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker()
Base = declarative_base()


def change_session_data(user, password, host):
    engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/evp?charset=latin1',
                           pool_size=20, max_overflow=0)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()