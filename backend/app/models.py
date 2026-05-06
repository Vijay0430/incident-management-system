from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Incident(Base):

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)

    component_id = Column(String)

    severity = Column(String)

    state = Column(String)

    start_time = Column(String)

    end_time = Column(String)

    mttr = Column(String)

class RCA(Base):

    __tablename__ = "rca"

    id = Column(Integer, primary_key=True)

    incident_id = Column(Integer)

    root_cause = Column(String)

    fix_applied = Column(String)

    prevention_steps = Column(String)
