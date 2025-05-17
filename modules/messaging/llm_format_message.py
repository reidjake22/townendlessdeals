from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from pathlib import Path
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")
# Create ChatGroq instance using the API key from environment variables
chat = ChatGroq(temperature=0.2, model="llama-3.3-70b-versatile", max_tokens=2000, api_key=groq_api_key)
history_file = Path("chat_history.json")

def format_with_llm(relevant_item_lists: dict):
    """
    has a dict of lists of SalesItems
    What it should do is take 
     and turn them into a single message using langchain
    """
    # Convert sale items to a format the LLM can understand
    items_text = ""
    for category, items in relevant_item_lists.items():
        items_text += f"\nCategory: {category}\n"
        for item in items:
            items_text += f"- {item['item_name']}: £{item['item_discounted_price']} (was £{item['item_price']})\n"
            price_history = item['metadata']['price_history']
            print(len(price_history))
            if len(price_history) > 1:
                if price_history[1]['item_discounted_price'] > item['item_discounted_price']:
                    items_text += f"  * Price dropped from £3{price_history[1]['item_discounted_price']} to £{item['item_discounted_price']}\n"
            else:
                items_text += f" This is a new deal"
            items_text +=f"  * {"damsonmadder.com/"+ item['item_url']}\n"

    
    # Create the prompt for the LLM
    prompt = f"""
    You are a helpful shopping assistant. Basically, what you do is tell the user about deals on a website that our servers track. It is not our website so call them they please! Make sure to refer to the site (it's the category!)
    follow the following rules:
    1. Mention every item by name, price and discount.
    2. Use emojis to make the message more engaging.
    3. act girlie-pop and use bratty emojis.
    4. At the end of the message highlighting some good discounts and items.
    5. Following the text element send a list of EVERY SINGLE ITEM with the following shape:
    A summary of all the deals is as follows:
    midi-dress: £50 (was £100)
    clutch-bag: £20 (was £40)
    ...
    6. DO NOT DO AND MANY MORE - YOU ABSOLUTELY MUST LIST EVERY ITEM
    7. capitalise the clothes names in the drop down list. GIVE EACH ITEM A RELEVANT EMOJI after the price description
    Format the following sale items into a friendly, 
    concise sms message that highlights every deal available. The message should be personal, 
    engaging, and mention all items by name and their prices and drops, use emojis whereever you like! Be fun.

    Here are the items on sale:
    {items_text}
    
    Create a message that would make someone excited to check out these deals.
    """
    print(prompt)
    # Send to LLM
    response = chat([HumanMessage(content=prompt)])
    print(response.content)
    return response.content


def save_message_to_json(user_name: str, message_content: str) -> None:

    """
    Save message to a local JSON file with role and content structure.
    Args:
        user_name: The name of the user receiving the message
        message_content: The content of the message
    """
    # Define the messages file path
    messages_file = Path('data/messages.json')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(messages_file), exist_ok=True)
    
    # Create message entry
    message_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_name,
        "role": "systemMessage",
        "content": message_content
    }
    
    # Load existing messages or create new messages list
    if messages_file.exists():
        try:
            with open(messages_file, 'r') as f:
                messages = json.load(f)
        except json.JSONDecodeError:
            messages = []
    else:
        messages = []
    
    # Add the new message and save
    messages.append(message_entry)
    with open(messages_file, 'w') as f:
        json.dump(messages, f, indent=2)