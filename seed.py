import psycopg2
import numpy as np
from database import DATABASE_URL

def setup_database():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # 1. Drop existing tables so we don't use old schemas
    print("Dropping old tables...")
    cursor.execute("DROP TABLE IF EXISTS users, courses CASCADE;")

    # 2. Create Fresh Tables
    print("Creating fresh tables...")
    cursor.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        skills_text TEXT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE courses (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        embedding TEXT
    );
    """)

    # 3. Insert a Mock User
    print("Inserting user data...")
    cursor.execute(
        "INSERT INTO users (name, skills_text) VALUES (%s, %s)",
        ("Zaid", "Python, PostgreSQL, LangChain, Big Data, Machine Learning")
    )

    # 4. Insert Mock Courses
    print("Inserting course data...")
    courses = [
        ("Advanced NLP & Multimodal AI", "Learn to build intelligent chatbots and analyze medical images using LLMs."),
        ("PostgreSQL Database Architecture", "Master relational databases, raw SQL, and vector storage."),
        ("Intro to Frontend Development", "Basic HTML, CSS, and simple web design."),
        ("Data Science with Python", "Analyze massive datasets using Pandas and PyTorch.")
    ]
    
    for title, desc in courses:
        # Generate a fake 384-dimensional vector string for testing
        mock_embedding = ",".join(map(str, np.random.rand(384)))
        cursor.execute(
            "INSERT INTO courses (title, description, embedding) VALUES (%s, %s, %s)",
            (title, desc, mock_embedding)
        )

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database setup complete!")

if __name__ == "__main__":
    setup_database()