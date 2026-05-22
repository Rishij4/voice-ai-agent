from app.tools.booking_tools import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)

tools = {
    "book": book_appointment,
    "cancel": cancel_appointment,
    "reschedule": reschedule_appointment
}