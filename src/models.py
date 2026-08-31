from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, JSON, Enum
import enum
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Coordination(Base):
    __tablename__ = 'Coordination'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    credits = Column(Integer, default=1000)
    # relationships
    tasks = relationship('AllocationTask', back_populates='coordination')

class AllocationTask(Base):
    __tablename__ = 'AllocationTask'
    id = Column(String, primary_key=True)
    status = Column(String, default='queued')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    progress = Column(Integer, default=0)
    error_log = Column(Text, nullable=True)
    result_summary = Column(Text, nullable=True)  # JSON stored as text
    # relationships
    bids = relationship('AuctionBid', back_populates='task')
    coordination_id = Column(Integer, ForeignKey('Coordination.id'), nullable=True)
    coordination = relationship('Coordination', back_populates='tasks')

class AuctionBid(Base):
    __tablename__ = 'AuctionBid'
    id = Column(String, primary_key=True)
    task_id = Column(String, ForeignKey('AllocationTask.id'))
    room_id = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)
    winner_coordination_id = Column(Integer, ForeignKey('Coordination.id'))
    loser_coordination_id = Column(Integer, ForeignKey('Coordination.id'))
    credits_spent = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    task = relationship('AllocationTask', back_populates='bids')
    winner = relationship('Coordination', foreign_keys=[winner_coordination_id])
    loser = relationship('Coordination', foreign_keys=[loser_coordination_id])

# Additional tables for rooms, teachers, classes, restrictions could be added similarly if needed.

class Room(Base):
    __tablename__ = 'Room'
    id = Column(String, primary_key=True)
    block_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    room_type = Column(String, nullable=False)
    is_accessible = Column(Boolean, default=True)
    features = Column(JSON, default=list)

class Class(Base):
    __tablename__ = 'Class'
    id = Column(String, primary_key=True)
    students_count = Column(Integer, nullable=False)
    room_type = Column(String, nullable=False)
    time_slot = Column(String, nullable=False)
    coordination_id = Column(String, nullable=False)
    urgency = Column(Integer, default=0)
    require_accessibility = Column(Boolean, default=False)

class DepartmentEnum(enum.Enum):
    ADMINISTRAÇÃO = "Administração"
    ENGENHARIA = "Engenharia"
    CIÊNCIAS = "Ciências"
    HUMANAS = "Humanas"

class Teacher(Base):
    __tablename__ = 'Teacher'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    department = Column(String, default="Geral")
    email = Column(String, nullable=True)
    subjects = Column(JSON, default=list)


class Restriction(Base):
    __tablename__ = 'Restriction'
    id = Column(String, primary_key=True)
    teacher_id = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    time_slot_id = Column(String, nullable=False)

class Allocation(Base):
    __tablename__ = 'Allocation'
    id = Column(String, primary_key=True)
    teacher_id = Column(String, nullable=False)
    room_id = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    shift = Column(String, nullable=False)
    sub_slot = Column(Integer, nullable=False)
    subject = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)



class SubslotTimeInterval(Base):
    __tablename__ = 'subslot_time_intervals'
    id = Column(String, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    shift = Column(String, nullable=False)
    class_number = Column(Integer, nullable=True)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    is_interval = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class User(Base):
    __tablename__ = 'User'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="docente", nullable=False)  # "gestor", "coordenador", "docente"
    department = Column(String, default="Geral", nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)



