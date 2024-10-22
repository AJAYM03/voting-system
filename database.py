import mysql.connector
from mysql.connector import Error
from config import Config  # Import your Config class

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        connection.commit()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_elections():
    """Fetch all scheduled elections from the database."""
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM elections WHERE status = 'scheduled'")
        return cursor.fetchall()  # Returns a list of tuples
    except Error as e:
        print(f"Error fetching elections: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
# Assuming you have a function that retrieves the election statistics

def get_election_statistics():
    query = """
    SELECT e.title AS election_title, u.username AS candidate_name, COUNT(v.id) AS total_votes
    FROM elections e
    JOIN candidates c ON e.id = c.election_id
    JOIN users u ON c.user_id = u.id
    LEFT JOIN votes v ON c.id = v.candidate_id
    GROUP BY e.id, c.id, u.username;
    """
    
    results = execute_query(query)
    
    # Debug line to see raw query results
    print("Raw query results:", results)  # Add this line here
    
    statistics = {}
    for row in results:
        election_title = row[0]
        candidate_name = row[1]
        total_votes = row[2] or 0  # Ensure total_votes is at least 0
        
        if election_title not in statistics:
            statistics[election_title] = []
        statistics[election_title].append({
            'candidate_name': candidate_name,
            'total_votes': total_votes
        })
    
    return statistics

def get_candidates_by_election(election_id):
    """Fetch candidates for a specific election."""
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT c.id, u.username AS name FROM candidates c JOIN users u ON c.user_id = u.id WHERE c.election_id = %s", (election_id,))
        return cursor.fetchall()  # Returns a list of tuples
    except Error as e:
        print(f"Error fetching candidates for election {election_id}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_votes_by_election(election_id):
    """Fetch votes for a specific election."""
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM votes WHERE election_id = %s", (election_id,))
        return cursor.fetchall()
    except Error as e:
        print(f"Error fetching votes for election {election_id}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def update_election_status(election_id, new_status):
    """Update the status of a specific election."""
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE elections SET status = %s WHERE id = %s", (new_status, election_id))
        connection.commit()
    except Error as e:
        print(f"Error updating election status for election {election_id}: {e}")
    finally:
        cursor.close()
        connection.close()
