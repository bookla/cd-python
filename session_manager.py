import uuid
import qr_generator
import os
from google.cloud import firestore

booth_name = "TEST BOOTH 1"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/Users/book/PycharmProjects/HIS-Christmas-Dinner/his-christmas-dinner-firebase-adminsdk-ub11c-865e9ecc40.json'


def create():
    session_id = uuid.uuid4().hex
    qr = qr_generator.get_qr(session_id)
    db = firestore.Client()
    collection = db.collection(u'sessions')
    collection.document(str(session_id)).set(
        {
            u'associatedEmail': "",
            u'boothName': booth_name,
            u'isActive': True,
            u'trigger': False,
        }
    )
    return session_id, qr


def deactivate(session_id):
    db = firestore.Client()
    collection = db.collection(u'sessions')
    collection.document(str(session_id)).set(
        {
            u'isActive': False,
        }
    , merge=True)


def is_triggered(session_id):
    db = firestore.Client()
    document = db.collection(u'sessions').document(str(session_id))

    data = document.get()
    if data.exists:
        data_dict = data.to_dict()
        if "trigger" in data_dict.keys():
            return data_dict["trigger"]
        else:
            print("trigger field doesn't seem to exist!")
            return False
    else:
        print("document does not exist!")
        return False


def get_email(session_id):
    db = firestore.Client()
    document = db.collection(u'sessions').document(str(session_id))

    data = document.get()
    if data.exists:
        data_dict = data.to_dict()
        if "associatedEmail" in data_dict.keys():
            return data_dict["associatedEmail"]
        else:
            print("email field does not exist!")
            return None
    else:
        print("document does not exist!")
        return None
