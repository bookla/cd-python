from os import listdir
from os.path import isfile, join
from google.cloud import firestore
from firebase_admin import auth
import csv

base_dir = "/Users/book/PycharmProjects/HIS-Christmas-Dinner"


def register_new_images(email, initial_list):
    current_image = [f for f in listdir(join(base_dir, 'images')) if isfile(join(join(base_dir, 'images'), f))]
    new_images = [f for f in current_image if f not in initial_list]
    with open(join(base_dir, "image-data.csv"), 'w+', newline='') as image_data:
        data_writer = csv.writer(image_data, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for image in new_images:
            data_writer.writerow([str(image), str(email)])
        image_data.close()
    return new_images


def get_initial():
    return [f for f in listdir(join(base_dir, 'images')) if isfile(join(join(base_dir, 'images'), f))]


def update_image_database(email, images_list):
    uid = auth.get_user_by_email(email).uid

    db = firestore.Client()
    collection = db.collection(u'users')
    document = collection.document(str(uid))
    user_doc = document.get()
    if user_doc.exists:
        data = user_doc.to_dict()
        if "images" in data.keys():
            new_data = ({} if data["images"] is None else data["images"])
            for image in images_list:
                new_data[image] = {
                    u'isUploaded': False,
                    u'imageLink': ""
                }
            collection.document(str(uid)).set(
                {
                    u'images': new_data
                }
            , merge=True)
