from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from databaseConfiguration.dbConfig import Config, DevelopmentConfig, ProductionConfig
from resources.employeeClass import Employee
from models.department import DepartmentModel
from models.employee import EmployeeModel


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
