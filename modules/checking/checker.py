import json
from ..scraping.scraper_tool import scrape_sale_page
from ..database.database import Database
from ..messaging.send_messages import update_all_users
def checker():
    """"
    This function is used to check the status of a website.
    """
    print("Checking for new sale items...")
    with open('modules/checking/checklist.json', 'r') as f:
        sites = json.load(f)
    new_sale_items = {}
    for site in sites:
        sale_items = scrape_sale_page(site)
        db = Database()
        site_new_sale_items = db.compare_against_db(sale_items, site)

        if site_new_sale_items:
            new_sale_items[site] = site_new_sale_items
            print(f"New sale items found for {site}: {site_new_sale_items}")
    if new_sale_items:
        print("New sale items found, updating end user.")
        update_all_users(new_sale_items)
