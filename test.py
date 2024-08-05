import duckdb

con = duckdb.connect('emergency_waitlist.duckdb')
result = con.execute('SELECT * FROM patients').fetchall()
print(result)
