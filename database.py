import psycopg2
from psycopg2.extras import RealDictCursor

# Replace with your actual PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:1234567890@localhost/course_recommender"

def get_db_connection():
    # RealDictCursor makes the database return rows as dictionaries instead of tuples
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()