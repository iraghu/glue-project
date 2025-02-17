import psycopg2
from psycopg2 import sql

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="rdstestinstance.c7am2q24ao0o.ap-south-1.rds.amazonaws.com",    # Database host
    dbname="rdstestdb",    # Database name
    user="quad",    # Username
    password="quad1777",  # Password
    port="5432"          # Default PostgreSQL port
     )

#rdsrefinedcluster
#rdsrefinedcluster.cluster-c7am2q24ao0o.ap-south-1.rds.amazonaws.com
#quadrefined
#qudaratic1777
#rdsrefinedcluster     quadrefined  qudaratic1777
# Create a cursor object using a context manager (it's automatically closed after block)
with conn.cursor() as cursor:
    # Example insert query
    createquery = """
    CREATE TABLE staff (
    id SERIAL PRIMARY KEY,  
    name VARCHAR(100),     
    email VARCHAR(100) UNIQUE, 
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP 
    );

    """
    insert_query = """
      INSERT INTO staff (name, email)
      VALUES ('John Doe', 'john.doe@example.com');
      """
    select_query = "SELECT * FROM employeeDuplicate;"
    cursor.execute(select_query)
    results = cursor.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Created At: {row[3]}")
    # Execute the insert query
    #cursor.execute(insert_query)
    
    # Commit the transaction
    conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully!")
