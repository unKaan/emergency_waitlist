from flask import Flask, request, jsonify
import duckdb
from models import db, Patient

app = Flask(__name__)

# I had to streamline some parts with my prior OLAP DB knowledge
con = duckdb.connect('emergency_waitlist.duckdb')

@app.route('/')
def index():
    patients = con.execute('SELECT * FROM patients ORDER BY severity DESC, wait_time').fetchall()
    return jsonify(patients)

@app.route('/admin', methods=['POST'])
def admin():
    # addne w
    name = request.form['name']
    severity = request.form['severity']
    wait_time = request.form['wait_time']
    con.execute('INSERT INTO patients (name, severity, wait_time) VALUES (?, ?, ?)', (name, severity, wait_time))
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(debug=True)

