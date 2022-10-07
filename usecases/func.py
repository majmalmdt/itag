from model.enterprise import Employee, Enterprise
from utils import app
from flask import request, jsonify
from functools import wraps
import jwt
from utils import *
import string
import random
from werkzeug.utils import secure_filename
import time
from datetime import datetime


# def welcome_mail(to):
#     msg = Message(
#         "Welcome to iTag",
#         recipients=[to],
#         html="<b>Welcome to iTag</b>")
#     mail.send(msg)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            print(token)

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        data = jwt.decode(
            token.replace('"', ''), app.config['SECRET_KEY'], algorithms=["HS256"])
        try:

            current_user = Enterprise.query.filter_by(
                public_key=data['public_id'], delete=0, status=1).first()
        except:
            return jsonify({'message': 'token is invalid'})
        if current_user is not None:
            return f(current_user, *args, **kwargs)
        return jsonify({'message': 'Enterprise not exist'})
    return decorator


def Store_Image(image):
    folder = 'enterprise/static/images/'
    file_extension = os.path.splitext(str(image.filename))[1]
    if file_extension not in ALLOWED_IMAGE_EXTENSIONS:
        return None
    N = 10
    res = '_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + \
        '_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    while Employee.query.filter_by(image=res).first() is not None:
        res = '_'+''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + \
            '_'+''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=N))
    filename = secure_filename(res+file_extension)
    image.save(folder+filename)
    return filename


def compare_time(time1):
    if int(time.strftime("%H:%M:%S").split(":")[0]) == int((time1).split(":")[0]):
        if int(time.strftime("%H:%M:%S").split(":")[1]) > int((time1).split(":")[1])+5:
            return True
        return False
    elif int(time.strftime("%H:%M:%S").split(":")[0]) > int((time1).split(":")[0])+1:
        return True
    elif int(time.strftime("%H:%M:%S").split(":")[1])+60 > int((time1).split(":")[1])+5:
        return True
    return False


def card_validity(validity, date):
    if int(time.strftime("%d/%m/%Y").split("/")[0]) > int((date).split("/")[0])+(validity-int(1)) and int(time.strftime("%d/%m/%Y").split("/")[1]) == int((date).split("/")[1]):
        print(int(time.strftime("%d/%m/%Y").split("/")
              [0]) > int((date).split("/")[0])+(validity-int(1)))
        return True
    return False


def WorkDuration(checkin, checkout):
    time_1 = datetime.strptime(checkin, "%H:%M:%S")
    time_2 = datetime.strptime(checkout, "%H:%M:%S")
    return str(time_2 - time_1)


def FilterAttendanceData(value):
    datelist = []
    filteredlist = []
    for val in value:
        datelist.append(val)
    for i in datelist:
        if int(i.date.split("/")[1]) == int(time.strftime("%d/%m/%Y").split("/")[1]) and int(i.date.split("/")[2]) == int(time.strftime("%d/%m/%Y").split("/")[2]):
            filteredlist.append(i)
    return [pun.values() for pun in filteredlist]


def TempIdAttendanceData(value):
    TempIDlist = []
    filteredlist = []
    for val in value:
        TempIDlist.append(val)
    for i in TempIDlist:
        if i.CardId_No.split("_")[0] == "TEM":
            filteredlist.append(i)
    return [pun.values() for pun in filteredlist]


def FilterTempIdAttendanceData(value):
    TempIDlist = []
    filteredlist = []
    for val in value:
        TempIDlist.append(val)
    for i in TempIDlist:
        if i.CardId_No.split("_")[0] == "TEM" and int(i.date.split("/")[1]) == int(time.strftime("%d/%m/%Y").split("/")[1]) and int(i.date.split("/")[2]) == int(time.strftime("%d/%m/%Y").split("/")[2]):
            filteredlist.append(i)
    return [pun.values() for pun in filteredlist]
