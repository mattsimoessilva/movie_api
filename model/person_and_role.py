from sqlalchemy import Column, Integer, ForeignKey
from model import Base

class PersonAndRole(Base):
    __tablename__ = "person_and_role"

    id = Column("pk_person_and_role", Integer, primary_key=True)
    person = Column(Integer, ForeignKey("person.pk_person", nullable=False))
    role = Column(Integer, ForeignKey("role.pk_role"), nullable=False)

    def __init__(self, person:int, role:int):
        self.person = person
        self.role = role