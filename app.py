from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Patient

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

@app.route('/')
def index():
    patients = Patient.query.order_by(Patient.severity.desc(), Patient.wait_time).all()
    return render_template('index.html', patients=patients)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        severity = request.form['severity']
        wait_time = request.form['wait_time']
        patient = Patient(name=name, severity=int(severity), wait_time=int(wait_time))
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('admin'))
    patients = Patient.query.all()
    return render_template('admin.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
