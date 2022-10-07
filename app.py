from utils import *
from model.enterprise import *
from flask import make_response, request, jsonify, make_response
from model.enterprise import *
from usecases.checks import *
from usecases.func import *
import jwt
import datetime
import string
import random


@app.route('/', methods=['GET'])
def index():
    return "Hello World!"


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    if emailcheck(email):
        enterprise = Enterprise.query.filter_by(email=email).first()
        if enterprise is not None:
            if enterprise.delete == 0:
                if enterprise.status == 1:
                    if bcrypt.check_password_hash(enterprise.password, password):
                        token = jwt.encode({'public_id': enterprise.public_key, 'exp': datetime.datetime.utcnow(
                        ) + datetime.timedelta(minutes=5000)}, app.config['SECRET_KEY'], "HS256")
                        resp = make_response(
                            jsonify({'token': token, "status": "success"}))
                        return resp
                    return jsonify({"status": "Incorrect Password"})
                return jsonify({"status": "Not Active"})
            return jsonify({"status": "Enterprise is Deleted"})
        return jsonify({"status": "No such enterprise"})
    return jsonify({"status": "Incorrect email format"})


@app.route('/logout', methods=['POST'])
@token_required
def logout(user):
    return jsonify({"status": "Logout"})


@app.route('/view_enterprise', methods=['POST'])
@token_required
def view_enterprise(user):
    return jsonify({"status": user.values()})


@app.route('/change_password', methods=['POST'])
@token_required
def change_password(user):
    if request.method == "POST":
        password = request.json['password']
        enterprise = Enterprise.query.filter_by(name=user.name).first()
        enterprise.password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        enterprise.save_to_db()
        return jsonify({"status": "Success"})
    else:
        return jsonify({"status": "Not a Post Request"})


@app.route('/update_enterprise', methods=['POST'])
@token_required
def update_enterprise(user):
    if request.method == "POST":
        phoneno = request.json['phoneno']
        enterprise = Enterprise.query.filter_by(name=user.name).first()
        if enterprise:
            enterprise.phoneno = phoneno
            enterprise.save_to_db()
            return jsonify({"status": "success"})
    else:
        return jsonify({"status": "Not a Post Request"})


@app.route('/change_enterprise_image', methods=['POST'])
@token_required
def change_enterprise_image(user):
    if request.method == "POST":
        path = Store_Image(request.files['image'])
        enterprise = Enterprise.query.filter_by(name=user.name).first()
        if enterprise:
            enterprise.image = path
            enterprise.save_to_db()
    else:
        return jsonify({"status": "Not a Post Request"})


@app.route('/add_employee', methods=['POST'])
@token_required
def add_employee(user):
    print(request.json)
    email = request.form['email']
    image = request.files['image']
    if emailcheck(email):
        employee = Employee.query.filter_by(email=email).first()
        if employee is None:
            path = Store_Image(image)
            if path is not None:
                if request.form['gender'] == "1":
                    gender = True
                else:
                    gender = False
                employee = Employee(name=request.form['name'], email=email, phone=request.form['phone'], position=request.form['position'],
                                    enterprise_id=user.id, department=request.form['department'], dob=request.form['dob'], gender=gender, image=path)
                employee.save_to_db()
                return jsonify({"status": "success"})
            return jsonify({"status": "Invalid File Format"})
        return jsonify({"status": "Employee already exists"})
    return jsonify({"status": "Invalid email"})


@app.route('/view_employee', methods=["POST"])
@token_required
def view_employee(user):
    id = request.json['id']
    emp_data = Employee.query.filter_by(id=id, enterprise_id=user.id).first()
    if emp_data:
        return jsonify({"status": emp_data.values()})
    return jsonify({"Status": "No such Employee"})


@app.route('/update_employee', methods=['POST'])
@token_required
def update_employee(user):
    data = request.form
    if emailcheck(data["email"]):
        employee = Employee.query.filter_by(
            email=data["email"], enterprise_id=user.id).first()
        if employee:
            employee.name = data["name"]
            employee.position = data["position"]
            employee.department = data["department"]
            employee.phone = data["phone"]
            path = Store_Image(request.files['image'])
            employee.image = path
            employee.save_to_db()
            return jsonify({"status": "updated"})
        return jsonify({"status": "Email doesn't Exist"})
    return jsonify({"status": "Invalid email"})


@app.route('/delete_employee', methods=['POST'])
@token_required
def delete_employee(user):
    data = request.json
    if emailcheck(data["email"]):
        employee = Employee.query.filter_by(
            email=data["email"], enterprise_id=user.id).first()
        if employee:
            employee.delete = True
            db.session.commit()
            return jsonify({"status": "deleted"})
        return jsonify({"status": "Email doesn't Exist"})
    return jsonify({"status": "Invalid email"})


@app.route('/employees_list', methods=['POST'])
@token_required
def employees_list(user):
    employees = Employee.query.filter_by(
        enterprise_id=user.id, delete=False).all()
    return jsonify([employee.values() for employee in employees])


@app.route('/employees_filter_list', methods=['POST'])
@token_required
def employees_filter_list(user):
    data = request.json
    employees = Employee.query.filter_by(
        enterprise_id=user.id, delete=False, department=data["department"]).all()
    print(employees)
    return jsonify([employee.values() for employee in employees])


@app.route('/getdatas', methods=['POST'])
@token_required
def getdatas(user):
    print(user.id)
    return jsonify({"datas": "all data"})


@app.route('/create_employee_id_card', methods=['POST'])
@token_required
def create_employee_id_card(user):
    N = 6
    data = request.json
    Employee_email = data['Employee_email']
    employee_data = Employee.query.filter_by(
        email=Employee_email, delete=False).first()
    if employee_data is None:
        return jsonify({"status": "No Employee found"})
    Id_check = Employee_ID_Card.query.filter_by(
        Employee_Id=employee_data.id).first()
    if Id_check:
        return jsonify({"status": "Already Exist"})
    rdmstr = 'EMP_'+''.join(random.choices(string.ascii_letters + string.digits, k=N)) + \
        ''.join(random.choices(string.ascii_letters + string.digits, k=N))
    while Employee_ID_Card.query.filter_by(Employee_Id_No=rdmstr).first() is not None:
        rdmstr = 'EMP_'+''.join(random.choices(string.ascii_letters + string.digits, k=N)) + \
            ''.join(random.choices(string.ascii_letters + string.digits, k=N))
    Employee_Id_No = rdmstr
    Id_Card = Employee_ID_Card(Employee_Id_No=Employee_Id_No, Name=employee_data.name,
                               Employee_Id=employee_data.id, Enterprise_id=employee_data.enterprise_id)
    Id_Card.save_to_db()
    return jsonify({"status": "ID created"})


@app.route('/Create_temp_ID_Card', methods=['POST'])
@token_required
def Create_temp_ID_Card(user):
    N = 6
    rdmstr = 'TEM_'+''.join(random.choices(string.ascii_letters + string.digits, k=N)) + \
        ''.join(random.choices(string.ascii_letters + string.digits, k=N))
    while Employee_TempID_Card.query.filter_by(Employee_RandomId_No=rdmstr).first() is not None:
        rdmstr = 'TEM_'+''.join(random.choices(string.ascii_letters + string.digits, k=N)) + \
            ''.join(random.choices(string.ascii_letters + string.digits, k=N))
    Employee_RandomId_No = rdmstr
    Temp_rdmstr = ''.join(random.choices(string.digits, k=N))
    while Employee_TempID_Card.query.filter_by(Employee_TempId_No=Temp_rdmstr).first() is not None:
        Temp_rdmstr = ''.join(random.choices(string.digits, k=N))
    Employee_TempId_No = Temp_rdmstr
    TempId_Card = Employee_TempID_Card(
        Employee_RandomId_No=Employee_RandomId_No, Employee_TempId_No=Employee_TempId_No, Enterprise_id=user.id)
    TempId_Card.save_to_db()
    return jsonify({"status": "TempID Created"})


@app.route('/Assign_temp_ID_Card', methods=['POST'])
@token_required
def Assign_temp_ID_Card(user):
    data = request.json
    email = data['Employee_email']
    Temp_Id_No = data['Temp_Id_No']
    Validity = data['Validity']
    Employee_data = Employee.query.filter_by(email=email, delete=False).first()
    if Employee_data is None:
        return jsonify({"status": "No Employee found"})
    Card_data = Employee_TempID_Card.query.filter_by(
        Employee_TempId_No=Temp_Id_No).first()
    Card_Assigned = Employee_TempID_Card_Assign(Name=Employee_data.name, Employee_RandomId_No=Card_data.Employee_RandomId_No, Employee_TempId_No=Temp_Id_No,
                                                Assigned_to=Employee_data.id, Assigned_at=time.strftime("%d/%m/%Y"), Validity=Validity, Enterprise_id=user.id, Employee_TempID_Card_rel=Card_data.id)
    Card_Assigned.save_to_db()
    return jsonify({"status": "TempID Assigned"})


@app.route('/TempID_Card_List', methods=['POST'])
@token_required
def TempID_Card_List(user):
    if request.method == "POST":
        new_list = []
        Temp_card_list = [card for card in Employee_TempID_Card.query.filter_by(
            Enterprise_id=user.id).all()]
        for card in Temp_card_list:
            for data in card.relationship()['Employee_TempID_Card_Assign_data']:
                x = False
                for dat in new_list:
                    if data.compare(dat):
                        x = True
                if x:
                    new_list.remove(dat)
                    new_list.append(data)
                else:
                    new_list.append(data)
        for dat in new_list.copy():
            if card_validity(dat.Validity, dat.Assigned_at):
                new_list.remove(dat)
        for temp_card in Temp_card_list.copy():
            for data in new_list:
                if data.card_compare(temp_card):
                    Temp_card_list.remove(temp_card)
        return jsonify({"values": [temp.values() for temp in Temp_card_list]})


@app.route('/Punching_data', methods=["GET"])
def Punching_data():
    Punching_Id = request.args.get('Punching_Id')
    if Punching_Id.split("_")[0] == "TEM":
        emp_data = Employee_TempID_Card_Assign.query.filter_by(
            Employee_RandomId_No=Punching_Id).first()
        # print(emp_data.Assigned_to)
        punched_data = PunchingData.query.filter_by(
            emp_id=emp_data.Assigned_to, date=str(time.strftime("%d/%m/%Y"))).first()
        if punched_data:
            if punched_data.check_out_time is None:
                if compare_time(punched_data.check_in_time):
                    punched_data.check_out_time = time.strftime("%H:%M:%S")
                    punched_data.CardId_No = Punching_Id
                    # time_1 = datetime.strptime(punched_data.check_in_time,"%H:%M:%S")
                    # time_2 = datetime.strptime(punched_data.check_out_time,"%H:%M:%S")
                    punched_data.work_duration = WorkDuration(
                        punched_data.check_in_time, punched_data.check_out_time)
                    punched_data.save_to_db()
                    return jsonify({"status": "Check out"})
                return jsonify({"status": "Try after some time"})
            return jsonify({"status": "Already Checked out"})
        print(emp_data.Validity)
        if card_validity(emp_data.Validity, emp_data.Assigned_at):
            print(card_validity(emp_data.Validity, emp_data.Assigned_at))

        new_punched_data = PunchingData(emp_id=emp_data.Assigned_to, name=emp_data.Name, CardId_No=Punching_Id, Enterprise_id=emp_data.Enterprise_id,
                                        Temp_id=emp_data.Employee_TempId_No, date=time.strftime("%d/%m/%Y"), check_in_time=time.strftime("%H:%M:%S"))
        new_punched_data.save_to_db()
        return jsonify({"status": "Checked in"})
    else:
        emp_data = Employee_ID_Card.query.filter_by(
            Employee_Id_No=Punching_Id).first()
        punched_data = PunchingData.query.filter_by(
            emp_id=emp_data.Employee_Id, date=str(time.strftime("%d/%m/%Y"))).first()
        if punched_data:
            if punched_data.check_out_time is None:
                if compare_time(punched_data.check_in_time):
                    punched_data.check_out_time = time.strftime("%H:%M:%S")
                    punched_data.CardId_No = Punching_Id
                    punched_data.work_duration = WorkDuration(
                        punched_data.check_in_time, punched_data.check_out_time)
                    punched_data.save_to_db()
                    return jsonify({"status": "Check out"})
                return jsonify({"status": "Try after some time"})
            return jsonify({"status": "Already Checked out"})
        new_punched_data = PunchingData(emp_id=emp_data.Employee_Id, name=emp_data.Name, CardId_No=Punching_Id,
                                        Enterprise_id=emp_data.Enterprise_id, Temp_id=None, date=time.strftime("%d/%m/%Y"), check_in_time=time.strftime("%H:%M:%S"))
        new_punched_data.save_to_db()
        return jsonify({"status": "Checked in"})


@app.route('/Punching_data_list', methods=['POST'])
@token_required
def Punching_data_list(user):
    data = PunchingData.query.filter_by(Enterprise_id=user.id).all()
    return jsonify([pun.values() for pun in data])


@app.route('/leave_emp_list', methods=['POST'])
@token_required
def leave_emp_list(user):
    employees = Employee.query.filter_by(
        enterprise_id=user.id, delete=False).all()
    datas = PunchingData.query.filter_by(
        Enterprise_id=user.id, date=time.strftime("%d/%m/%Y")).all()
    y_time = time.strftime("%d/%m/%Y")
    d = int((y_time).split("/")[0])-1
    ystdatas = PunchingData.query.filter_by(
        Enterprise_id=user.id, date=time.strftime(str(d)+"/%m/%Y")).all()
    ystleaved = []
    for employee in employees:
        x = True
        for data in ystdatas:
            if employee.compare(data.emp_id):
                x = False
        if x:
            ystleaved.append(employee)
    leaved = []
    for employee in employees:
        x = True
        for data in datas:
            if employee.compare(data.emp_id):
                x = False
        if x:
            leaved.append(employee)
    return jsonify({"today": [leavedata.values() for leavedata in leaved], "yesterday": [leavedata.values() for leavedata in ystleaved]})


@app.route('/leave_emp_filter_list', methods=['POST'])
@token_required
def leave_emp_filter_list(user):
    data = request.json
    employees = Employee.query.filter_by(
        enterprise_id=user.id, delete=False, department=data["department"]).all()
    datas = PunchingData.query.filter_by(
        Enterprise_id=user.id, date=time.strftime("%d/%m/%Y")).all()
    leaved = []
    for employee in employees:
        x = True
        for data in datas:
            if employee.compare(data.emp_id):
                x = False
        if x:
            leaved.append(employee)
    return jsonify({"status": [leavedata.values() for leavedata in leaved]})


@app.route('/employee_attendance', methods=['POST'])
@token_required
def employee_attendance(user):
    data = request.json
    Employee_id = data['id']
    employee_data = Employee.query.filter_by(id=Employee_id).first()
    emp_data = PunchingData.query.filter_by(
        Enterprise_id=user.id, emp_id=employee_data.id).all()
    if emp_data:
        return jsonify({"status": [pun.values() for pun in emp_data]})
    return jsonify({"status": "No Data"})


@app.route('/filtered_employee_attendance', methods=['POST'])
@token_required
def filtered_employee_attendance(user):
    data = request.json
    Employee_id = data['id']
    employee_data = Employee.query.filter_by(id=Employee_id).first()
    emp_data = PunchingData.query.filter_by(
        Enterprise_id=user.id, emp_id=employee_data.id).all()
    if emp_data:
        return jsonify({"status": FilterAttendanceData(emp_data)})
    else:
        return jsonify({"status": "No Data"})


@app.route('/Employee_TempId_Attendance', methods=['POST'])
@token_required
def Employee_TempId_Attendance(user):
    data = request.json
    Employee_id = data['id']
    employee_data = Employee.query.filter_by(id=Employee_id).first()
    emp_data = PunchingData.query.filter_by(
        Enterprise_id=user.id, emp_id=employee_data.id).all()
    if emp_data:
        return jsonify({"status": TempIdAttendanceData(emp_data)})
    return jsonify({"status": "No Data"})


@app.route('/Filtered_Employee_TempId_Attendance', methods=['POST'])
@token_required
def Filtered_Employee_TempId_Attendance(user):
    data = request.json
    Employee_id = data['id']
    employee_data = Employee.query.filter_by(id=Employee_id).first()
    emp_data = PunchingData.query.filter_by(
        Enterprise_id=user.id, emp_id=employee_data.id).all()
    if emp_data:
        return jsonify({"status": FilterTempIdAttendanceData(emp_data)})
    return jsonify({"status": "No Data"})


@app.route('/Employees_Count', methods=['POST'])
@token_required
def Employees_Count(user):
    if request.method == "POST":
        employees = Employee.query.filter_by(
            enterprise_id=user.id, delete=False).count()
        employee = PunchingData.query.filter_by(
            Enterprise_id=user.id, date=time.strftime("%d/%m/%Y")).count()
        return jsonify({"Total": employees, "Present": employee})
    return jsonify({"status": "Not a POST request"})


@app.route('/Add_Schedule', methods=['POST'])
@token_required
def Add_Schedule(user):
    if request.method == "POST":
        data = request.json
        title = data['title']
        startdate = data['startdate']
        enddate = data['enddate']
        new_schedule = Schedule(
            title=title, startdate=startdate, enddate=enddate)
        return "success"


if __name__ == '__main__':
    app.run()
