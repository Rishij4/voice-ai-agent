from app.services.nlp_service import extract_patient_and_doctor
import dateparser

from app.memory.conversation_state import (
    save_conversation_state,
    get_conversation_state,
    clear_conversation_state
)
from app.services.llm_service import generate_response

from app.tools.booking_tools import (
    book_appointment,
    cancel_appointment,
    reschedule_appointment
)


def process_user_query(user_input, language="English"):
    session_id = "default_user"

    state = get_conversation_state(session_id)

    if not state:
        state = {}


    lower_input = user_input.lower()


    if "book" in lower_input:
        details = extract_patient_and_doctor(user_input)

        patient = details["patient"] or "Guest"

        doctor = details["doctor"] or "Dr Sharma"
        parsed_time = dateparser.parse(user_input)

        if parsed_time:
            parsed_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        else:
            parsed_time = "2026-05-22 17:00"


        try:
            tool_response = book_appointment(
                patient=patient,
                doctor=doctor,
                time=parsed_time
            )

        except Exception as e:
            return generate_response(
                f"Booking failed: {str(e)}",
                language
            )

        print("[INFO] Checking availability")
        print("[INFO] Booking completed")
        state["last_appointment"] = tool_response["appointment"]

        save_conversation_state(session_id, state)

        return generate_response(
            f"{patient}, your appointment with {doctor} has been booked for {parsed_time}.",
            language
        )

    elif "cancel" in lower_input:

        appointment = state.get("last_appointment")

        if not appointment:
            return generate_response(
                "No appointment found to cancel.",
                language
            )

        try:
            tool_response = cancel_appointment(
                appointment["id"]
            )

            clear_conversation_state(session_id)

            return generate_response(
                "Your appointment has been cancelled successfully.",
                language
            )

        except Exception as e:
            return generate_response(
                f"Cancellation failed: {str(e)}",
                language
            )

    elif "reschedule" in lower_input:

        appointment = state.get("last_appointment")

        if not appointment:
            return generate_response(
                "No appointment found to reschedule.",
                language
            )

        parsed_time = dateparser.parse(user_input)

        if parsed_time:
            new_time = parsed_time.strftime("%Y-%m-%d %H:%M")
        else:
            return generate_response(
                "Please provide a valid new date and time.",
                language
            )

        try:
            tool_response = reschedule_appointment(
                appointment["id"],
                new_time
            )

            appointment["time"] = new_time

            save_conversation_state(session_id, state)

            return generate_response(
                f"Your appointment has been rescheduled to {new_time}.",
                language
            )

        except Exception as e:
            return generate_response(
                f"Reschedule failed: {str(e)}",
                language
            )

    else:

        return generate_response(
            user_input,
            language
        )