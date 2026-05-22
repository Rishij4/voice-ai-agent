from sqlalchemy import Column, Integer, String
from app.models.database import Base

class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient = Column(String)

    doctor = Column(String)

    time = Column(String)
    status = Column(String)
    language = Column(String)
    created_at = Column(String)