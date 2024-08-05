from flask import Flask, request, redirect, url_for
# had to streamline DB
import duckdb
import os

app = Flask(__name__)

@app.route('/')
def index():
    with duckdb.connect('emergency_waitlist.duckdb') as con:
        patients = con.execute('SELECT * FROM patients ORDER BY severity DESC, wait_time').fetchall()

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/css/styles.css">
        <title>Emergency Waitlist</title>
    </head>
    <body>
        <header>
            <h1>Emergency Room Waitlist</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/admin">Admin Panel</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Current Patients</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Severity</th>
                        <th>Wait Time (minutes)</th>
                    </tr>
                </thead>
                <tbody>
    """

    for patient in patients:
        html_content += f"""
        <tr>
            <td>{patient[1]}</td>
            <td>{patient[2]}</td>
            <td>{patient[3]}</td>
        </tr>
        """

    html_content += """
                </tbody>
            </table>
        </main>
        <footer>
            <p>&copy; 2024 Emergency Waitlist</p>
        </footer>
    </body>
    </html>
    """

    return html_content

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        severity = int(request.form['severity'])
        wait_time = int(request.form['wait_time'])
        with duckdb.connect('emergency_waitlist.duckdb') as con:
            con.execute('INSERT INTO patients (name, severity, wait_time) VALUES (?, ?, ?)', (name, severity, wait_time))
        return redirect(url_for('admin'))

    with duckdb.connect('emergency_waitlist.duckdb') as con:
        patients = con.execute('SELECT * FROM patients').fetchall()

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="/static/css/styles.css">
        <title>Admin Panel - Emergency Waitlist</title>
    </head>
    <body>
        <header>
            <h1>Emergency Room Waitlist</h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/admin">Admin Panel</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h2>Admin Panel</h2>
            <form method="post">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="severity">Severity:</label>
                <input type="number" id="severity" name="severity" min="1" max="10" required>
                
                <label for="wait_time">Wait Time (minutes):</label>
                <input type="number" id="wait_time" name="wait_time" min="0" required>
                
                <button type="submit">Add Patient</button>
            </form>

            <h3>All Patients</h3>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Severity</th>
                        <th>Wait Time (minutes)</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
    """

    for patient in patients:
        html_content += f"""
        <tr>
            <td>{patient[1]}</td>
            <td>{patient[2]}</td>
            <td>{patient[3]}</td>
            <td>
                <form method="post" action="/delete/{patient[0]}" style="display:inline;">
                    <button type="submit">Delete</button>
                </form>
            </td>
        </tr>
        """

    html_content += """
                </tbody>
            </table>
        </main>
        <footer>
            <p>&copy; 2024 Emergency Waitlist</p>
        </footer>
    </body>
    </html>
    """

    return html_content

@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    with duckdb.connect('emergency_waitlist.duckdb') as con:
        con.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
