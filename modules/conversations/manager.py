# modules/conversations/manager.py
from .database import MessageDatabase
from .personality import get_personality_prompt
from ..messaging.llm_format_message import format_with_llm
import json

class ConversationManager:
    def __init__(self):
        self.db = MessageDatabase()
    
    def add_message(self, phone_number, role, content, referenced_items=None):
        """Add a message to the conversation history"""
        self.db.store_message(phone_number, role, content, referenced_items)
    
    def build_conversation_context(self, phone_number):
        """Build the context for the LLM from conversation history"""
        # Get conversation history and last system message
        history = self.db.get_conversation_history(phone_number, limit=10)
        
        # Format the conversation history for the LLM
        formatted_history = []
        for msg in history:
            formatted_history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Always include the personality system message at the beginning
        personality = get_personality_prompt()
        system_message = {
            "role": "system",
            "content": personality
        }
        
        # If we have a recent system message with sale info, include that too
        last_system = self.db.get_last_system_message(phone_number)
        if last_system and "referenced_items" in last_system and last_system["referenced_items"]:
            items_data = json.loads(last_system["referenced_items"])
            system_message["content"] += f"\n\nRecently mentioned items: {json.dumps(items_data, indent=2)}"
        
        return [system_message] + formatted_history
    
    def process_user_message(self, phone_number, user_message):
        """Process a user message and generate a response"""
        # Add the user message to history
        self.add_message(phone_number, "user", user_message)
        
        # Build conversation context
        context = self.build_conversation_context(phone_number)
        
        # Generate response using a conversation-specific function
        response = self.generate_conversation_response(context, user_message)
        
        # Store the assistant's response
        self.add_message(phone_number, "assistant", response)
        
        return response

    def generate_conversation_response(self, context, user_message):
        """Generate a response to a user message using conversation context"""
        from langchain_groq import ChatGroq
        import os
        from langchain.schema import HumanMessage, SystemMessage, AIMessage
        
        # Get API key
        groq_api_key = os.environ.get("GROQ_API_KEY")
        
        # Create ChatGroq instance
        chat = ChatGroq(
            temperature=0.7,  # Higher temperature for more creative responses
            model="llama-3.3-70b-versatile",
            max_tokens=1000,
            api_key=groq_api_key
        )
        
        # Convert context to LangChain message format
        messages = []
        for msg in context:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
                
        # Generate response
        response = chat(messages)
        
        return response.content
    
    def add_system_notification(self, phone_number, content, referenced_items):
        """Add a system notification about new deals"""
        self.add_message(phone_number, "system", content, referenced_items)