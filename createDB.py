# import duckdb
#
# con = duckdb.connect('emergency_waitlist.db')
#
# # patients table
# con.execute('''
# CREATE TABLE patients (
#     id INTEGER PRIMARY KEY,
#     name VARCHAR,
#     severity INTEGER,
#     wait_time INTEGER
# )
# ''')
import pandas as pd
import duckdb

# Load the CSV file into a Pandas DataFrame
df = pd.read_csv('data/patients.csv')

# Connect to DuckDB
con = duckdb.connect('emergency_waitlist.duckdb')

# Create the patients table if it doesn't exist
con.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    severity INTEGER,
    wait_time INTEGER
)
''')

# Insert data from DataFrame into DuckDB table
con.execute('INSERT INTO patients SELECT * FROM df')

print("Data imported successfully.")
