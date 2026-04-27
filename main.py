from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
import psycopg2
from database import get_db_connection
from schemas import RecommendRequest, RecommendResponse, CourseResponse
from ai_layer import extract_skills, generate_embedding
from recommender import get_top_recommendations

app = FastAPI(title="Skills Utilization Platform API")

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.post("/api/recommend", response_model=RecommendResponse)
def recommend_courses(
    request: RecommendRequest, 
    conn = Depends(get_db_connection)  # Inject raw connection
):
    # Open a raw SQL cursor
    cursor = conn.cursor()
    user_text = ""

    # 1. Handle User Input via raw SQL
    if request.user_id:
        cursor.execute("SELECT skills_text FROM users WHERE id = %s;", (request.user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_text = user["skills_text"]
        
    elif request.user_text:
        user_text = request.user_text
    else:
        raise HTTPException(status_code=400, detail="Must provide either user_id or user_text")

    # 2. AI Layer
    skills = extract_skills(user_text)
    skills_joined = " ".join(skills)
    user_embedding = generate_embedding(skills_joined)

    # 3. Retrieve Courses via raw SQL
    cursor.execute("SELECT id, title, description, embedding FROM courses;")
    all_courses = cursor.fetchall()

    # 4. Rank and format
    top_matches = get_top_recommendations(user_embedding, all_courses)

    recommended_courses = [
        CourseResponse(
            id=match["course"]["id"],
            title=match["course"]["title"],
            description=match["course"]["description"],
            similarity_score=match["score"]
        )
        for match in top_matches
    ]

    return RecommendResponse(
        extracted_skills=skills,
        recommended_courses=recommended_courses,
        explanation="Recommendations generated using raw SQL and cosine similarity."
    )