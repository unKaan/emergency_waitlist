import pandas as pd
import duckdb

users_df = pd.read_csv('data/users.csv')

con = duckdb.connect('Patients.duckdb')

con.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    full_name VARCHAR,
    username VARCHAR,
    location VARCHAR,
    age INTEGER
)
''')

con.execute('INSERT INTO users SELECT * FROM users_df')

print("User data imported successfully.")
