from dotenv import load_dotenv
import os

load_dotenv()  # This loads variables from a .env file into the environment

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_MODELS = [
    "gemma2-9b-it",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

#print(GROQ_API_KEY)
