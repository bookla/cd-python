import csv
import os
import uuid
import pickle
import time
from os.path import join
from google.cloud import firestore
from google.cloud import storage
from firebase_admin import auth
import firebase_admin

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/Users/book/PycharmProjects/HIS-Christmas-Dinner/his-christmas-dinner-firebase-adminsdk-ub11c-865e9ecc40.json'

base_dir = "/Users/book/PycharmProjects/HIS-Christmas-Dinner"

file_type = "png"

firebase_admin.initialize_app()

with open(join(base_dir, "image-data.csv"), "w+", newline='') as data:
    data.close()

while True:
    excluded_files = []
    try:
        with open(join(base_dir, "complete.pkl"), 'rb') as exclude_data:
            excluded_files = pickle.load(exclude_data)
            exclude_data.close()
    except FileNotFoundError:
        print("No file")
    file_list = []
    with open(join(base_dir, "image-data.csv"), "r+", newline='') as image_data:
        reader = csv.reader(image_data, delimiter=' ', quotechar='|')
        for file in reader:
            if file not in excluded_files:
                file_list.append(file)
    for each_file in file_list:
        print()
        file_name = each_file[0]
        email = each_file[1]
        print(file_name)
        print(email)
        uid = auth.get_user_by_email(email).uid
        print(uid)

        image_id = uuid.uuid4().hex + "." + file_type

        client = storage.Client(project="his-christmas-dinner")
        bucket = client.get_bucket("his-christmas-dinner.appspot.com")
        blob = storage.Blob(str(uid) + "/" + image_id, bucket)
        with open(join(join(base_dir, "images"), file_name), "rb") as image_file:
            blob.upload_from_file(image_file, content_type="image/" + file_type)
            image_file.close()

        current_data = firestore.Client().collection(u'users').document(str(uid)).get().to_dict()
        if file_name in current_data["images"].keys():
            current_data["images"][file_name]["isUploaded"] = True
            current_data["images"][file_name]["imageLink"] = image_id

        firestore.Client().collection(u'users').document(str(uid)).set(current_data)

        excluded_files.append(each_file)

        with open(join(base_dir, "complete.pkl"), 'wb+') as exclude_data:
            pickle.dump(excluded_files, exclude_data)
            exclude_data.close()
    time.sleep(1)
