from sqlalchemy.orm import Session
from datetime import datetime

from app.models.database import SessionLocal
from app.models.appointment import Appointment


def book_appointment(patient, doctor, time):

    db: Session = SessionLocal()

    try:

        booking_time = datetime.strptime(
            time,
            "%Y-%m-%d %H:%M"
        )

        if booking_time < datetime.now():

            db.close()

            return {
                "status": "failed",
                "message": "Cannot book past time slot"
            }

    except:
        pass

    existing = db.query(Appointment).filter(
        Appointment.doctor == doctor,
        Appointment.time == time
    ).first()

    if existing:

        db.close()

        return {
            "status": "failed",
            "message": "Slot unavailable",
            "alternative_slots": [
                "2026-05-22 18:00",
                "2026-05-22 19:00",
                "2026-05-22 20:00"
            ]
        }

    appointment = Appointment(
        patient=patient,
        doctor=doctor,
        time=time,
        status="Booked",
        language="English",
        created_at=str(datetime.now())
    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    result = {
        "id": appointment.id,
        "patient": appointment.patient,
        "doctor": appointment.doctor,
        "time": appointment.time,
        "status": appointment.status
    }

    db.close()

    return {
        "status": "success",
        "appointment": result
    }


def cancel_appointment(appointment_id):

    db: Session = SessionLocal()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:

        db.close()

        return {
            "status": "failed",
            "message": "Appointment not found"
        }

    appointment.status = "Cancelled"

    db.commit()

    db.close()

    return {
        "status": "cancelled",
        "appointment_id": appointment_id
    }


def reschedule_appointment(appointment_id, new_time):

    db: Session = SessionLocal()

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:

        db.close()

        return {
            "status": "failed",
            "message": "Appointment not found"
        }

    existing = db.query(Appointment).filter(
        Appointment.doctor == appointment.doctor,
        Appointment.time == new_time
    ).first()

    if existing:

        db.close()

        return {
            "status": "failed",
            "message": "Requested slot unavailable",
            "alternative_slots": [
                "2026-05-22 18:00",
                "2026-05-22 19:00"
            ]
        }

    appointment.time = new_time

    appointment.status = "Rescheduled"

    db.commit()

    db.refresh(appointment)

    result = {
        "id": appointment.id,
        "patient": appointment.patient,
        "doctor": appointment.doctor,
        "time": appointment.time,
        "status": appointment.status
    }

    db.close()

    return {
        "status": "rescheduled",
        "appointment": result
    }