import duckdb

con = duckdb.connect('emergency_waitlist.db')

# patients table
con.execute('''
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    severity INTEGER,
    wait_time INTEGER
)
''')
