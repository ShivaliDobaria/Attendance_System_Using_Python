import csv
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from django.shortcuts import render
import re

# Create your views here.
from generate_report.models import Students, Batch


def home(request):
    batch_names = Batch.objects.all()
    return render(request, 'home.html', {'objectlist': batch_names})


def upload(request):
    if request.method == 'POST':
        all_numbers = []
        years_dict = dict()
        trainer_name = request.POST.get("txtTrainerName")
        trainer_email = request.POST.get("trainerEmail")
        batch_id = request.POST.get('batch_name')
        for f in request.FILES.getlist('filesToUpload'):
            try:
                which_day = f.name.split('_')[1].split('.')[0]
                f = open("C:/Users/Shivali/python_projects/attendance_system/Media/Chat_Files/" + f.name, mode='r',
                         encoding='UTF-8')
                lines = f.readlines()
                count = 0
                for line in lines:
                    c_file_number = re.findall(r'\d{10}', line)
                    if c_file_number:
                        all_numbers.append(c_file_number)
                        years_dict[which_day] = c_file_number
            except Exception as e:
                print(e)
            finally:
                f.close()
        get_datafrom_database(all_numbers, trainer_name, trainer_email, batch_id, years_dict)
    return render(request, 'success.html')


def get_datafrom_database(all_numbers, trainer_name, trainer_email, batch_id, years_dict):
    studentdata = Students.objects.filter(batch_name=batch_id)
    create_report(studentdata, trainer_name, trainer_email, all_numbers, years_dict)


def create_report(studentdata, trainer_name, trainer_email, all_numbers, years_dict):
    file_path = 'C:/Users/Shivali/python_projects/attendance_system/Media/report.csv'
    if os.path.exists(file_path):
        os.remove(file_path)

    writer = csv.writer(open('C:/Users/Shivali/python_projects/attendance_system/Media/report.csv', 'w', newline=''), delimiter=',',
                       )
    writer.writerow(['first_name', 'phone_number', 'email_id', 'Status'])
    for i in studentdata:
        if i.phone_number in (item for sublist in all_numbers for item in sublist):
            status = 'Present'
        else:
            status = 'Absent'
        writer.writerow([i.first_name, i.phone_number, i.email_id, status])

    send_Email(trainer_name, trainer_email)


def send_Email(trainer_name, trainer_email):
    fromaddr = "shivali95dobaria@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = trainer_email

    # storing the subject
    msg['Subject'] = "Attendance Report"

    # string to store the body of the mail
    body = "Hi "+trainer_name + ", \n Attached the attendance report"
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "report.xls"
    attachment = open('C:/Users/Shivali/python_projects/attendance_system/Media/report.xls', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload(attachment.read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "password goes here")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, trainer_email, text)

    # terminating the session
    s.quit()

