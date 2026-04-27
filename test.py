from fastapi.testclient import TestClient
from main import app

# Create a test client
client = TestClient(app)

def test_recommendation_endpoint():
    # Define the payload we want to send
    payload = {
        "user_text": "I know Python, SQL, and Machine Learning."
    }

    # Send a POST request to our API
    response = client.post("/api/recommend", json=payload)

    # 1. Check that the request was successful (HTTP 200 OK)
    assert response.status_code == 200

    # 2. Parse the JSON response
    data = response.json()

    # 3. Verify the structure of the response
    assert "extracted_skills" in data
    assert "recommended_courses" in data
    assert "explanation" in data

    print("✅ Test passed! The API is responding correctly.")

if __name__ == "__main__":
    test_recommendation_endpoint()