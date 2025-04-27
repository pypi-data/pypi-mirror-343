
from langchain_groq import ChatGroq
from .config import GROQ_API_KEY
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
class LLMInterface:
    def __init__(self, models):
        self.models = models
        self.llms = {
            model: ChatGroq(model_name=model, temperature=0.2, groq_api_key=GROQ_API_KEY)
            for model in models
        }

    def query_model(self, model_name, prompt):
        llm = self.llms[model_name]
        return llm.invoke(prompt).content