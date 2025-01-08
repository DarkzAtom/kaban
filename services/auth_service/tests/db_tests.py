import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def test_connection():
    try:
        # Establish the connection
        conn = psycopg2.connect(
            dbname="auth_db",
            user="auth_user",
            password="admin",  # Replace with your actual password
            host="localhost"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Create a cursor object
        cur = conn.cursor()

        # Execute a simple query
        cur.execute("SELECT version();")

        # Fetch the result
        version = cur.fetchone()[0]
        print(f"Successfully connected to PostgreSQL. Version: {version}")

        # Close communication with the database
        cur.close()
        conn.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


if __name__ == "__main__":
    test_connection()