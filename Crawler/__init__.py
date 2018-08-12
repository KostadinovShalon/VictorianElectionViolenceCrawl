from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+mysqldb://data_feeder:Arp48dEx@coders.victorianelectionviolence.uk/evp')
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)

__all__ = ['spiders', 'utils', 'Session', 'engine', 'Base']
