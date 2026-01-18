from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import Config
import json

class SimpleLLM:
    
    def __init__(self, temperature=0.7):
        self.llm = ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model_name=Config.GROQ_MODEL,
            temperature=temperature,
        )
    
    def chat(self, user_message, system_message=None):
        messages = []
        
        if system_message:
            messages.append(SystemMessage(content=system_message))
        
        messages.append(HumanMessage(content=user_message))
        
        response = self.llm.invoke(messages)
        return response.content
    
    def extract_json(self, user_message, system_message=None):
        if not system_message:
            system_message = "You are a helpful assistant. Respond with valid JSON only."
        else:
            system_message += "\n\nIMPORTANT: Respond with valid JSON only, no extra text."
        
        response = self.chat(user_message, system_message)
        
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        return json.loads(response)


_llm = None

def get_llm(temperature=0.7):
    global _llm
    if _llm is None:
        _llm = SimpleLLM(temperature=temperature)
    return _llm
