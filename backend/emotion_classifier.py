from langchain_groq import ChatGroq
from config.settings import GROQ_API_KEY


class EmotionClassifier:
    def __init__(self):
        self.model = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY, temperature=0.0)

    def classify(self, message: str) -> str:
        prompt = f"Classify the emotion of this text into one word (sad, anxious, angry, stressed, happy, neutral): {message}"
        emotion = self.model.invoke(prompt).content.lower()
        return emotion
