from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
Base = declarative_base()



class Material(Base):
    __tablename__ = 'material_resources'

    material_csr_code = Column(String(20), primary_key=True, nullable=False)
    material_name = Column(String(1500), nullable=False)
    material_measure = Column(String(25), default='kg')

  

    def __repr__(self):
        return f"Material({self.material_csr_code}, {self.material_name})"

class MaterialsCustomer(Base):
    __tablename__ = 'material_resources_customer'

    material_csr_code = Column(String(20), ForeignKey('material_resources.material_csr_code'), primary_key=True)
    material_name = Column(String(1500), nullable=False)
    material_measure = Column(String(25), default='kg')
    customer = Column(String(50), nullable=False)
    date = Column(DateTime, default=func.now())

  

    def __repr__(self):
        return f"MaterialsCustomer({self.customer}, {self.material_csr_code})"
