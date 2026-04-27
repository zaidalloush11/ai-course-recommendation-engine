from app import app
from models import db, Course

flask_course = Course(
    title="Python Web Mastery with Flask",
    description="Learn how to build professional backends, APIs, and web applications using the Flask framework and PostgreSQL."
)

with app.app_context():
    db.session.add(flask_course)
    db.session.commit()
    print("Flask course added to the database!")