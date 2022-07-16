from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from databaseConfiguration.dbConfig import Config, DevelopmentConfig, ProductionConfig
from resources.employeeClass import Employee

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


class EmployeeModel(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(), nullable=False)
    gender = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phoneNumber = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    level = db.Column(db.String(), nullable=False)
    yoe = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    department_name = db.Column(db.String(), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def createRecord(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def employeeExists(cls, Employeeemail):
        record = cls.query.filter_by(email=Employeeemail)

        if record.first():
            return True
        else:
            return False

    @classmethod
    def getAllEmployees(cls):
        return cls.query.all()

    @classmethod
    def getEmployeeById(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def EditEmployeeById(cls, id, name=None, gender=None, email=None, phone=None, title=None,
                         level=None, yoe=None, dptid=None, dptname=None, salary=None):
        record = cls.query.filter_by(id=id).first()

        if record:
            record.fullName = name
            record.gender = gender
            record.email = email
            record.phoneNumber = phone
            record.title = title
            record.level = level
            record.yoe = yoe
            record.salary = salary
            record.department_name = dptname
            record.department_id = dptid
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def deleteEmployeeById(cls, id):
        record = cls.query.filter_by(id=id)

        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False


class DepartmentModel(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=True, unique=True)
    employee = db.relationship(
        'EmployeeModel', backref='department', lazy=True)

    def createRecord(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def departmentExists(cls, departmentName):
        record = cls.query.filter_by(name=departmentName)

        if record.first():
            return True
        else:
            return False

    @classmethod
    def getAllDepartments(cls):
        return cls.query.all()

    @classmethod
    def getDepartmentById(cls, departmentId):
        return cls.query.filter_by(id=departmentId).first()

    @classmethod
    def EditDepartmentById(cls, id, name=None):
        record = cls.query.filter_by(id=id).first()

        if record:
            record.name = name
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def deleteDepartmentById(cls, id):
        record = cls.query.filter_by(id=id)

        if record.first():
            record.delete()
            db.session.commit()
            return True
        else:
            return False


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/departments', methods=['GET', 'POST'])
def departments():

    allDepartments = DepartmentModel.getAllDepartments()

    if request.method == 'POST':

        departmentName = request.form['fullName']

        if DepartmentModel.departmentExists(departmentName):
            flash('Department already exists', 'danger')
            return redirect(url_for('departments'))
        else:
            record = DepartmentModel(name=departmentName)
            record.createRecord()
            flash('Department added successfully', 'success')
            return redirect(url_for('departments'))

    return render_template('departments.html', allDepts=allDepartments)


@app.route('/department/employees/<int:id>', methods=['GET', 'POST'])
def departmentViewEmployees(id):

    departmentEmployees = DepartmentModel.getDepartmentById(id)

    employees = departmentEmployees.employee

    return render_template('departmentEmployees.html', department_employees=employees,
                           department=departmentEmployees)


@app.route('/department/edit/<int:id>', methods=['POST'])
def editDepartment(id):
    if request.method == 'POST':
        name = request.form['name']

        update = DepartmentModel.EditDepartmentById(id=id, name=name)

        if update:
            flash('Department updated successfully', 'success')
            return redirect(url_for('departments'))
        else:
            flash('Update error', 'danger')
            return redirect(url_for('departments'))


@app.route('/department/delete/<int:id>', methods=['POST'])
def deleteDepartment(id):

    delete = DepartmentModel.deleteDepartmentById(id)

    if delete:

        flash('Department deleted successfully', 'success')
        return redirect(url_for('departments'))

    else:

        flash('Delete error', 'danger')
        return redirect(url_for('departments'))


@app.route('/employees', methods=['GET', 'POST'])
def employees():

    allDepartments = DepartmentModel.getAllDepartments()

    allEmployees = EmployeeModel.getAllEmployees()

    if request.method == 'POST':
        name = request.form['fullName']
        gender = request.form['gender']
        employeeEmail = request.form['email']
        phone = request.form['phone']
        employeeTitle = request.form['title']
        employeeLevel = int(request.form['level'])
        employeeYoe = int(request.form['yoe'])
        departmentName = request.form['department']
        departmentId = request.form['department']

        pay = Employee(level=employeeLevel, yoe=employeeYoe)

        employeeSalary = pay.calculateSalary()

        if EmployeeModel.employeeExists(employeeEmail):
            flash('Employee already exists', 'danger')
            return redirect(url_for('employees'))
        else:
            employee = EmployeeModel(fullName=name, gender=gender, email=employeeEmail, phoneNumber=phone, title=employeeTitle,
                                     department_id=departmentId, level=employeeLevel, yoe=employeeYoe,
                                     salary=employeeSalary,
                                     department_name=departmentName)

            employee.createRecord()

            flash('Employee added successfully', 'success')

            return redirect(url_for('employees'))

    return render_template('employees.html', allDepts=allDepartments, allEmps=allEmployees)


@app.route('/employee/edit/<int:id>', methods=['POST'])
def editEmployee(id):
    if request.method == 'POST':
        name = request.form['fullName']
        gender = request.form['gender']
        employeeEmail = request.form['email']
        phone = request.form['phone']
        employeeTitle = request.form['title']
        employeeLevel = int(request.form['level'])
        employeeYoe = int(request.form['yoe'])
        departmentName = request.form['department']
        departmentId = request.form['department']

        pay = Employee(level=employeeLevel, yoe=employeeYoe)

        employeeSalary = pay.calculateSalary()

        update = EmployeeModel.EditEmployeeById(id=id, name=name, gender=gender,
                                                email=employeeEmail, phone=phone,
                                                title=employeeTitle, level=employeeLevel, yoe=employeeYoe,
                                                dptid=departmentId,
                                                dptname=departmentName,
                                                salary=employeeSalary)

        if update:
            flash('Employee updated successfully', 'success')
            return redirect(url_for('employees'))
        else:
            flash('Update error', 'danger')
            return redirect(url_for('employees'))


@app.route('/employee/delete/<int:id>', methods=['POST'])
def deleteEmployee(id):

    delete = EmployeeModel.deleteEmployeeById(id)

    if delete:

        flash('Employee deleted successfully', 'success')
        return redirect(url_for('employees'))

    else:

        flash('Delete error', 'danger')
        return redirect(url_for('employees'))


if __name__ == "__main__":
    app.run(debug=True)
