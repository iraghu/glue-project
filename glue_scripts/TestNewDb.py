import psycopg2
from psycopg2 import sql

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="rdsrefinedcluster.cluster-c7am2q24ao0o.ap-south-1.rds.amazonaws.com",    # Database host
    dbname="postgres",    # Database name
    user="quadrefined",    # Username
    password="qudaratic1777",  # Password
    port="5423"          # Default PostgreSQL port
     )

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
      VALUES ('John Doe789', 'john.doe789@example.com');
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
