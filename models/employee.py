from crud import db


class EmployeeModel(db.Model):

    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(), nullable=False)
    lastName = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    yoe = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phoneNumber = db.Column(db.String(), nullable=False)
    department_name = db.Column(db.String(), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    def create_record(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getAllEmployees(cls):
        return cls.query.all()

    @classmethod
    def getEmployeeById(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def editEmployeeById(cls, id, firstName=None, lastName=None, title=None, level=None, yoe=None,
                         gender=None, email=None, phone=None, dptname=None, dptid=None):
        record = cls.query.filter_by(id=id).first()

        if record:
            record.firstName = firstName
            record.lastName = lastName
            record.title = title
            record.level = level
            record.yoe = yoe
            record.gender = gender
            record.email = email
            record.phoneNumber = phone
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
