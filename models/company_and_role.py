from sqlalchemy import Column, String, Integer, ForeignKey
from models import Base

class CompanyAndRole(Base):
    __tablename__ = 'company_and_role'

    id = Column("pk_company_and_role", Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.pk_company"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.pk_role"), nullable=False)
