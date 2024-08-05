from flask import Flask, request, jsonify, render_template, redirect, url_for
import duckdb
import os

app = Flask(__name__)

# I had to streamline some parts with my prior OLAP DB knowledge
con = duckdb.connect('emergency_waitlist.duckdb')


con.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    severity INTEGER,
    wait_time INTEGER
)
''')
con.close()

@app.route('/')
def index():
    con = duckdb.connect('emergency_waitlist.duckdb')
    patients = con.execute('SELECT * FROM patients ORDER BY severity DESC, wait_time').fetchall()
    return render_template('index.html', patients=patients)
    con.close

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        severity = int(request.form['severity'])
        wait_time = int(request.form['wait_time'])
        con = duckdb.connect('emergency_waitlist.duckdb')
        con.execute('INSERT INTO patients (name, severity, wait_time) VALUES (?, ?, ?)', (name, severity, wait_time))
        con.close()
        return redirect(url_for('admin'))

    # Retrieve all patients
    con = duckdb.connect('emergency_waitlist.duckdb')
    patients = con.execute('SELECT * FROM patients').fetchall()
    con.close()
    return render_template('admin.html', patients=patients)

@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    con = duckdb.connect('emergency_waitlist.duckdb')
    con.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    con.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
