import configparser

import sqlalchemy as db

config = configparser.ConfigParser()
config.read('settings.ini')

engine = db.create_engine(config['APP']['DATABASE_URL'])
conn = engine.connect()
metadata = db.MetaData()

User = db.Table('Users', metadata,
    db.Column('ID', db.Integer, primary_key=True),
    db.Column('Name', db.String(255)),
    db.Column('Warns', db.String(255))
)