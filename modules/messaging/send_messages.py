import json
from ..models import SaleItem
from .llm_format_message import format_with_llm
from twilio.rest import Client
import time
from dotenv import load_dotenv
import os
# Load environment variables from .env file

load_dotenv()
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUMBER")
print(twilio_number)
def generate_content(new_sale_items: dict, user: dict) -> list[SaleItem]:
    """
    This function is used to generate content to send to the user.
    """
    relevant_item_lists = { key: items for key, items in new_sale_items.items() if key in user['interests'] }
    return relevant_item_lists

def update_all_users(new_sale_items: dict) -> None:
    """
    This function is used to update the users with new sale items.
    """
    with open('modules/messaging/users.json', 'r') as f:
        users = json.load(f)
    # users is a dictionary with user_name as key
    for user_name, user in users.items():
        print(user_name)
        print(user)
        print(user['interests'])
        relevant_item_lists = generate_content(new_sale_items, user)
        if relevant_item_lists:
            send_message(relevant_item_lists, user)

def send_message(relevant_item_lists: dict, user: dict) -> None:
    """
    This function is used to send a message to the user.
    Split long messages intelligently if they exceed 1600 characters.
    """
    print(f"Sending message to {user['name']}: {relevant_item_lists}")
    message_body = format_with_llm(relevant_item_lists)
    
    # Twilio credentials
    
    client = Client(account_sid, auth_token)
    
    # Split message if needed
    message_parts = split_message(message_body)
    
    # Send each part
    for i, part in enumerate(message_parts):
        prefix = f"[{i+1}/{len(message_parts)}] " if len(message_parts) > 1 else ""
        print(twilio_number)
        print(user['phone_number'])
        message = client.messages.create(
            body = prefix + part,
            from_=twilio_number,
            to=user['phone_number']
        )
        time.sleep(1)  # Avoid hitting Twilio rate limits
        print(f"Message part {i+1}/{len(message_parts)} sent")
    
    print("All message parts sent")

def split_message(message: str, max_length: int = 1500) -> list[str]:
    """
    Split a message into parts that are each under the maximum length.
    Try to split at logical break points like newlines when possible.
    
    Args:
        message: The full message to split
        max_length: Maximum length of each part
        
    Returns:
        List of message parts
    """
    # If message is already short enough, return it as is
    if len(message) <= max_length:
        return [message]
    
    parts = []
    remaining = message
    
    while len(remaining) > max_length:
        # Try to find a good split point near the max_length
        # Look for newlines first
        split_index = remaining[:max_length].rfind('\n')
        
        # If no good newline, try periods or other punctuation
        if split_index == -1 or split_index < max_length * 0.5:  # Avoid tiny splits
            split_index = remaining[:max_length].rfind('. ')
            
        # If still no good split point, try spaces
        if split_index == -1 or split_index < max_length * 0.5:
            split_index = remaining[:max_length].rfind(' ')
            
        # If all else fails, hard split at max_length
        if split_index == -1:
            split_index = max_length
        
        # Add the part and continue with the rest
        parts.append(remaining[:split_index].strip())
        remaining = remaining[split_index:].strip()
    
    # Add the last part
    if remaining:
        parts.append(remaining)
        
    return parts

