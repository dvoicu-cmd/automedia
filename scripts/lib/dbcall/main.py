import mariadb

# Create a connection to the remote MariaDB database
conn = mariadb.connect(host='10.10.2.3', port=3306, user='py_interface', password='sshDB#532', database='emails')

# Create a cursor object
cur = conn.cursor()

print("Writing query")

# Write the query
query = "INSERT INTO emails (email, password) VALUES (danATsampletext.com, passwd)"

# Execute the query
cur.execute(query)

print("Query Executed on remote")

# Close the cursor and connection
cur.close()
conn.close()
