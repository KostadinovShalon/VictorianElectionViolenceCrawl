from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

host = 'coders.victorianelectionviolence.uk'
user = 'data_feeder'
password = 'Arp48dEx'

engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/evp?charset=latin1')
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)

__all__ = ['spiders', 'utils', 'Session', 'engine', 'Base']
