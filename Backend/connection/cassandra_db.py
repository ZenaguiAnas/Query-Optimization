from cassandra.cluster import Cluster

def connect_to_cassandra():
    try:
        cluster = Cluster(['127.0.0.1'])  
        session = cluster.connect()

        # Create a keyspace
        keyspace_query = "CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}"
        session.execute(keyspace_query)

        # Use the keyspace
        session.set_keyspace('my_keyspace')

        return session
    except Exception as e:
        print(f"Error connecting to Cassandra: {e}")
        return None

def create_table(session):
    try:
        table_query = """
            CREATE TABLE IF NOT EXISTS queries (
                text TEXT,
            )
        """
        session.execute(table_query)
        print("Table created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_data(session, text):
    try:
        insert_query = f"""
            INSERT INTO queries (text)
            VALUES ('{text}')
        """
        session.execute(insert_query)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error inserting data: {e}")

def query_data(session):
    try:
        select_query = "SELECT * FROM queries"
        result = session.execute(select_query)

        for row in result:
            print(row)
    except Exception as e:
        print(f"Error querying data: {e}")

def close_connection(cluster):
    try:
        cluster.shutdown()
        print("Connection closed.")
    except Exception as e:
        print(f"Error closing connection: {e}")

if __name__ == "__main__":
    session = connect_to_cassandra()

    if session:
        create_table(session)

        insert_data(session, "<s>[INST] SELECT * FROM customers WHERE email_address LIKE '%gmail.com%'; [/INST]  Here are a few ways you could optimize the query:\n\n1. Use an index on the `email_address` column:\n```\nCREATE INDEX idx_email_address ON customers (email_address);\n```\nThis will speed up the search for customers with email addresses containing 'gmail.com'.\n [FINAL] SELECT * FROM customers WHERE email_address LIKE '%gmail.com%'</s>")

        query_data(session)

        # Close the connection
        close_connection(session.cluster)
