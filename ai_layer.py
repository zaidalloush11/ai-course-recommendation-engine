import numpy as np

def extract_skills(text: str) -> list[str]:
    """
    Extracts core skills from a user's text profile.
    Replace with your LLM extraction logic.
    """
    if not text:
        return []
    # Mock implementation: Splits by comma
    return [skill.strip() for skill in text.split(",") if skill.strip()]

def generate_embedding(text: str) -> list[float]:
    """
    Converts text into a vector representation.
    Replace with your embedding model (e.g., OpenAIEmbeddings or SentenceTransformers).
    """
    # Mock implementation: Returns a random 384-dimensional vector
    return np.random.rand(384).tolist()