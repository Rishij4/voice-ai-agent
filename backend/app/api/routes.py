from fastapi import APIRouter
from app.tools.booking_tools import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment,
)

router = APIRouter()

@router.get("/book")
def book(patient:str, doctor:str, time:str):
    return book_appointment(patient, doctor, time)

@router.get("/cancel")
def cancel(appointment_id:int):
    return cancel_appointment(appointment_id)

@router.get("/reschedule")
def reschedule(appointment_id:int, new_time:str):
    return reschedule_appointment(appointment_id, new_time)