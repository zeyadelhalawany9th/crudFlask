from crud import db


class DepartmentModel(db.Model):

    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    location = db.Column(db.String(), nullable=False)
    employee = db.relationship(
        'EmployeeModel', backref='department', lazy=True)

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getAllDepartments(cls):
        return cls.query.all()

    @classmethod
    def getDepartmentById(cls, dpt_id):
        return cls.query.filter_by(id=dpt_id).first()

    @classmethod
    def editDepartmentById(cls, id, name=None, location=None):
        record = cls.query.filter_by(id=id).first()

        if record:
            record.name = name
            record.location = location

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
