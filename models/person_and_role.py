from sqlalchemy import Column, Integer, ForeignKey
from models import Base

class PersonAndRole(Base):
    __tablename__ = "person_and_role"

    id = Column("pk_person_and_role", Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey("person.pk_person"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.pk_role"), nullable=False)