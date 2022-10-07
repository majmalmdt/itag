from utils import db


class Enterprise(db.Model):
    __tablename__ = 'enterprise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    public_key = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    delete = db.Column(db.Boolean(), default=False)
    status = db.Column(db.Boolean(), default=True)
    image = db.Column(db.String(100), nullable=True)
    phoneno = db.Column(db.String(100), nullable=True)

    def __init__(self, name, email, password, public_key, delete, status, image, phoneno):
        self.name = name
        self.email = email
        self.password = password
        self.public_key = public_key
        self.delete = delete
        self.status = status
        self.image = image
        self.phoneno = phoneno

    def __repr__(self):
        return f"Enterprise('{self.id}','{self.name}', '{self.email}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            "name": self.name,
            "email": self.email,
            "image": self.image,
            "phoneno": self.phoneno
        }


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(100), nullable=True)
    gender = db.Column(db.Boolean(), default=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    delete = db.Column(db.Boolean(), default=False)
    enterprise_id = db.Column(db.Integer, db.ForeignKey('enterprise.id'))
    department = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    enterprise = db.relationship(
        'Enterprise', backref=db.backref('employees', lazy=True))
    employee_id_card_data = db.relationship('Employee_ID_Card')

    def __init__(self, name, dob, gender, image, email, position, enterprise_id, department, phone):
        self.name = name
        self.email = email
        self.position = position
        self.enterprise_id = enterprise_id
        self.department = department
        self.phone = phone
        self.dob = dob
        self.gender = gender
        self.image = image

    def __repr__(self):
        return f"Employee('{self.name}', '{self.email}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def compare(self, id):
        if self.id == id:
            return True
        return False

    def values(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position,
            "department": self.department,
            "dob": self.dob,
            "gender": self.gender,
            "image": self.image

        }

    def relationship(self):
        return {
            "employee_id_card_data": self.employee_id_card_data
        }


class Employee_ID_Card(db.Model):
    __tablename__ = 'Employee_ID_Card'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Employee_Id_No = db.Column(db.String(100), nullable=True)
    Employee_Id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    Enterprise_id = db.Column(db.Integer, nullable=True)
    punching_data = db.relationship('PunchingData')

    def __repr__(self):
        return f"Employee_ID_Card('{self.id}', '{self.Employee_Id_No}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            "Employee_Id_No": self.Employee_Id_No,
            "Enterprise_id": self.Enterprise_id,
            "Name": self.Name
        }

    def relationship(self):
        return {
            "punching_data": self.punching_data
        }


class Employee_TempID_Card(db.Model):
    __tablename__ = 'Employee_TempID_Card'
    id = db.Column(db.Integer, primary_key=True)
    Employee_RandomId_No = db.Column(db.String(100), nullable=True)
    Employee_TempId_No = db.Column(db.String(100), nullable=True)
    Enterprise_id = db.Column(db.Integer, nullable=True)
    Employee_TempID_Card_Assign_data = db.relationship(
        'Employee_TempID_Card_Assign')

    def __repr__(self):
        return f"Employee_TempID_Card('{self.id}', '{self.Employee_RandomId_No}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            "Employee_RandomId_No": self.Employee_RandomId_No,
            "Employee_TempId_No": self.Employee_TempId_No,
            "Enterprise_id": self.Enterprise_id
        }

    def relationship(self):
        return {
            "Employee_TempID_Card_Assign_data": self.Employee_TempID_Card_Assign_data
        }


class Employee_TempID_Card_Assign(db.Model):
    __tablename__ = 'Employee_TempID_Card_Assign'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Employee_RandomId_No = db.Column(db.String(100), nullable=True)
    Employee_TempId_No = db.Column(db.String(100), nullable=True)
    Assigned_to = db.Column(db.Integer, nullable=True)
    Assigned_at = db.Column(db.String(100), nullable=True)
    Validity = db.Column(db.Integer, nullable=True)
    Enterprise_id = db.Column(db.Integer, nullable=True)
    Employee_TempID_Card_rel = db.Column(
        db.Integer, db.ForeignKey('Employee_TempID_Card.id'))
    punching_data = db.relationship('PunchingData')

    def __repr__(self):
        return f"Employee_TempID_Card_Assign('{self.Employee_TempId_No}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            "Name": self.Name,
            "Employee_RandomId_No": self.Employee_RandomId_No,
            "Employee_TempId_No": self.Employee_TempId_No,
            "Assigned_to": self.Assigned_to,
            "Validity": self.Validity,
            "Enterprise_id": self.Enterprise_id
        }

    def relationship(self):
        return {
            "punching_data": self.punching_data
        }

    def compare(self, obj):
        if self.Employee_TempId_No == obj.Employee_TempId_No:
            return True
        return False

    def card_compare(self, obj):
        if self.Employee_RandomId_No == obj.Employee_RandomId_No:
            return True
        return False


class PunchingData(db.Model):
    __tablename__ = 'PunchingData'
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey(
        'Employee_ID_Card.id'), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(100), nullable=True)
    CardId_No = db.Column(db.String(100), nullable=True)
    Enterprise_id = db.Column(db.Integer, nullable=True)
    Temp_id = db.Column(db.Integer, db.ForeignKey(
        'Employee_TempID_Card_Assign.id'), nullable=True)
    check_in_time = db.Column(db.String(100), nullable=True)
    check_out_time = db.Column(db.String(100), nullable=True)
    work_duration = db.Column(db.String(100), nullable=True)

    def __init__(self, emp_id, date, check_in_time, CardId_No, Enterprise_id, Temp_id, name):
        self.emp_id = emp_id
        self.name = name
        self.date = date
        self.check_in_time = check_in_time
        self.CardId_No = CardId_No
        self.Enterprise_id = Enterprise_id
        self.Temp_id = Temp_id

    def __repr__(self):
        return f"PunchingData('{self.emp_id}', '{self.date}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            'id': self.id,
            'name': self.name,
            'emp_id': self.emp_id,
            'date': self.date,
            'check_in_time': self.check_in_time,
            'check_out_time': self.check_out_time,
            'Temp_id': self.Temp_id,
            'Enterprise_id': self.Enterprise_id,
            'CardId_No': self.CardId_No,
            'work_duration': self.work_duration
        }


class Schedule(db.Model):
    __tablename__ = 'Schedule'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.String(100), nullable=True)
    end_date = db.Column(db.String(100), nullable=True)
    delete = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"Schedule('{self.id}', '{self.title}')"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def values(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_date': self.start_date,
            'end_date': self.end_date
        }
