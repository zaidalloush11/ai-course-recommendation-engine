import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def get_top_recommendations(user_embedding: list[float], courses: list[dict], top_n: int = 3):
    if not courses:
        return []

    user_vec = np.array(user_embedding).reshape(1, -1)
    recommendations = []

    for course in courses:
        if course["embedding"]:
            course_vec = np.array([float(x) for x in course["embedding"].split(",")]).reshape(1, -1)
            
            score = cosine_similarity(user_vec, course_vec)[0][0]
            
            recommendations.append({
                "course": course,
                "score": float(score)
            })

    recommendations.sort(key=lambda x: x["score"], reverse=True)
    return recommendations[:top_n]