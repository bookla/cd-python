import uuid
from google.cloud import firestore
from firebase_admin import auth
import firebase_admin
import os
from os.path import join
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
import smtplib

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'/Users/book/PycharmProjects/HIS-Christmas-Dinner/his-christmas-dinner-firebase-adminsdk-ub11c-865e9ecc40.json'

firebase_admin.initialize_app()


def user_exists(email):
    try:
        uid = auth.get_user_by_email(email)
        return True
    except:
        return False


def create_user(email):
    access_code = str(uuid.uuid4().hex)[:12]

    user = auth.create_user(
        email=str(email),
        email_verified=False,
        password=str(access_code),
        display_name=str(email),
        disabled=False)

    uid = user.uid

    db = firestore.Client()
    db.collection(u'users').document(str(uid)).create(
        {
            u'code': str(access_code),
            u'images': {}
        }
    )
    return email, access_code


def send_create_email(email, code):
    try:
        if len(email) == 0:
            return
        from_addr = "book_la@harrowschool.ac.th"
        password = ""
        to_addr = email
        smtp_server = "smtp.office365.com"

        # email object that has multiple part:
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = Header('Photo Booth Account Creation', 'utf-8').encode()

        body = "Welcome to Photo Booth. Please use the following link to access your photos. Please do not share this link with anyone as it will give them access to your photos. (You may, however, wish to share this with someone who you would like to share the photos with)\n\n Link: http://his-christmas-dinner.web.app/login.html?email={0}&code={1}. \n\n\n If the link above doesn't work please go to http://his-christmas-dinner.web.app/login.html and enter the following credentials: \n Email: {0}\n Access Code: {1}\n\n\n\n".format(email, code)

        print(body)

        msg_content = MIMEText(body, "plain", "utf-8")
        msg.attach(msg_content)

        server = smtplib.SMTP(smtp_server, 587)
        server.ehlo()
        server.starttls()
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
    except:
        print("SOME ERROR TOO BAD CONTINUE WORKING")