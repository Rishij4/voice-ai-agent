import spacy

nlp = spacy.load("en_core_web_sm")


def extract_patient_and_doctor(text):

    doc = nlp(text)

    patient = None
    doctor = None

    words = text.split()

    for i, word in enumerate(words):

        if word.lower() == "dr" and i + 1 < len(words):
            doctor = f"Dr {words[i + 1]}"

    for ent in doc.ents:

        if ent.label_ == "PERSON":

            if doctor and ent.text in doctor:
                continue

            patient = ent.text
            break

    return {
        "patient": patient,
        "doctor": doctor
    }