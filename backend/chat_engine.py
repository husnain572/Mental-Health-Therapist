# # # backend/chat_engine.py

# # from langchain_groq import ChatGroq  # Llama 3.1 8B Instant wrapper
# # from backend.rag_engine import RAGEngine
# # from backend.emotion_classifier import EmotionClassifier
# # from backend.safety_guard import SAFETY_WARNING

# # class ChatEngine:
# #     def __init__(self):
# #         # Initialize Llama model via ChatGroq
# #         self.llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.4)

# #         # Simple memory: store conversation history in a list
# #         self.memory = []

# #         # RAG knowledge base
# #         self.rag = RAGEngine()

# #         # Emotion detection
# #         self.emotion_model = EmotionClassifier()

# #     def get_response(self, user_input: str) -> str:
# #         # 1️⃣ Detect emotion
# #         emotion = self.emotion_model.classify(user_input)

# #         # 2️⃣ Search RAG knowledge base
# #         tips = self.rag.search(user_input)[0]

# #         # 3️⃣ Generate final prompt
# #         prompt = (
# #             f"User feels {emotion}. "
# #             f"Provide empathetic support and include advice: {tips}. "
# #             f"Message: {user_input}"
# #         )

# #         # 4️⃣ Generate response from Llama 3.1
# #         response = self.llm.invoke(prompt).content


# #         # 5️⃣ Append to memory
# #         self.memory.append({"user": user_input, "bot": response})

# #         return response
# class ChatEngine:
#     def __init__(self):
#         self.llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.4)
#         self.memory = []  # store conversation history
#         self.rag = RAGEngine()
#         self.emotion_model = EmotionClassifier()

#     def get_response(self, user_input: str) -> str:
#         # Detect emotion
#         emotion = self.emotion_model.classify(user_input)

#         # Get RAG advice
#         tips = self.rag.search(user_input)

#         # Construct conversational prompt with history
#         history_text = ""
#         for turn in self.memory[-5:]:  # keep last 5 turns
#             history_text += f"User: {turn['user']}\nBot: {turn['bot']}\n"

#         prompt = (
#             f"{history_text}"
#             f"User feels {emotion}. Provide empathetic support and advice: {tips}.\n"
#             f"User: {user_input}\nBot:"
#         )

#         # Generate response
#         response = self.llm.invoke(prompt)
#         bot_reply = response.content if hasattr(response, "content") else str(response)

#         # Save to memory
#         self.memory.append({"user": user_input, "bot": bot_reply})

#         return bot_reply
# backend/chat_engine.py

from langchain_groq import ChatGroq  # Llama 3.1 8B Instant wrapper
from backend.rag_engine import RAGEngine
from backend.emotion_classifier import EmotionClassifier

class ChatEngine:
    def __init__(self):
        # Initialize Llama model
        self.llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.4)

        # Memory to simulate conversation
        self.memory = []

        # RAG knowledge base
        self.rag = RAGEngine()

        # Emotion detection
        self.emotion_model = EmotionClassifier()

    def get_response(self, user_input: str) -> str:
        # Detect emotion
        emotion = self.emotion_model.classify(user_input)

        # Get RAG advice
        tips = self.rag.search(user_input)

        # Build prompt with conversation history
        history_text = ""
        for turn in self.memory[-5:]:  # include last 5 turns
            history_text += f"User: {turn['user']}\nBot: {turn['bot']}\n"

        prompt = (
            f"{history_text}"
            f"User feels {emotion}. Provide empathetic support and advice: {tips}.\n"
            f"User: {user_input}\nBot:"
        )

        # Generate response
        response_obj = self.llm.invoke(prompt)
        bot_reply = response_obj.content if hasattr(response_obj, "content") else str(response_obj)

        # Save to memory
        self.memory.append({"user": user_input, "bot": bot_reply})

        return bot_reply
