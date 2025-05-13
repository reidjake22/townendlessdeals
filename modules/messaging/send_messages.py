import json
from ..models import SaleItem
def generate_content(new_sale_items: dict, user: dict) -> list[SaleItem]:
    """
    This function is used to generate content to send to the user.
    """
    relevant_item_lists = { key: items for key, items in new_sale_items.items() if key in user['interests'] }
    return relevant_item_lists

def send_message(relevant_item_lists: dict, user: dict) -> None:
    """
    This function is used to send a message to the user.
    """
    print(f"Sending message to {user['name']}: {relevant_item_lists}")

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