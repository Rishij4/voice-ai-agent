conversation_states = {}


def save_conversation_state(session_id, state):

    conversation_states[session_id] = state


def get_conversation_state(session_id):

    return conversation_states.get(session_id, {})


def clear_conversation_state(session_id):

    if session_id in conversation_states:

        del conversation_states[session_id]