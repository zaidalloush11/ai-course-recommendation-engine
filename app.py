from flask import Flask, request, jsonify
from models import db, Course

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567890@localhost/course_recommender'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    # We import here, INSIDE the function, to avoid the circular import error
    from recommender import recommend_courses_semantic
    from ai_layer import extract_skills_from_text

    data = request.get_json()
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    # 1. AI Skill Extraction
    extracted_skills = extract_skills_from_text(user_text)

    # 2. Semantic Recommendation
    results = recommend_courses_semantic(user_text)

    # 3. Format Response
    recommendations_list = []
    for course, score in results:
        recommendations_list.append({
            "course_title": course.title,
            "description": course.description,
            "match_score": f"{round(score * 100)}%"
        })

    return jsonify({
        "input_text": user_text,
        "extracted_skills": extracted_skills,
        "recommendations": recommendations_list
    })

if __name__ == "__main__":
    app.run(debug=True)