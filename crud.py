import imp
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/departments')
def departments():
    return render_template('departments.html')


@app.route('/employees')
def employees():
    return render_template('employees.html')


if __name__ == "__main__":
    app.run(debug=True)
