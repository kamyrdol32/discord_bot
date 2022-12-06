import configparser

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, Session

config = configparser.ConfigParser()
config.read('settings.ini')

engine = create_engine(config['APP']['DATABASE_URL'])
Base = declarative_base()
session = Session(engine)


class Job (Base):
    __tablename__ = 'Jobs'
    ID = Column(Integer, primary_key=True)
    Job_ID = Column(String(256))
    Company = Column(String(256))
    Name = Column(String(256))
    Salary = Column(String(256))
    Contract = Column(String(256))
    Link = Column(String(512))

    def __init__(self, Job_ID, Company, Name, Salary, Contract, Link):
        self.Job_ID = Job_ID
        self.Company = Company
        self.Name = Name
        self.Salary = Salary
        self.Contract = Contract
        self.Link = Link

    def __repr__(self):
        return f"Job('{self.company}', '{self.name}', '{self.salary}', '{self.contract}', '{self.link}')"

    def __str__(self):
        return f"{self.company} - {self.name} - {self.salary} - {self.contract} - {self.link}"


Base.metadata.create_all(engine)