from ...models import SaleItem
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, TypedDict, Union
import requests
def damson_madder_scraper() -> list[SaleItem]:
    """
    Scrape the Damson Madder website for sale items.

    Returns:
        list[SaleItem]: A list of SaleItem dictionaries containing the scraped data.
    """
    url = "https://damsonmadder.com/collections/sale"
    sale_items = []
    sale_items = scrape_dm_sale_page(url, sale_items)
    return sale_items

def scrape_dm_sale_page(url: str, sale_items: list[SaleItem]) -> list[SaleItem]:
    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.select_one('.collection-grid')["data-next-url"]
        print(next_page)
        for item in soup.select('.product-card'):
            item_id = int(item['data-product-id'])
            item_name = item.select_one('.product-title').text.strip()
            #item_description = item.select_one('.product-card__description').text.strip()
            item_price = float(item.select_one('.sale-price').text.strip().replace('£', ''))
            item_discounted_price = float(item.select_one('.price').text.strip().replace('£', ''))
            item_url = item.select_one('a')['href']
            
            sale_item = SaleItem(
                item_id=item_id,
                item_name=item_name,
                item_description="",
                item_price=item_price,
                item_discounted_price=item_discounted_price,
                item_url=item_url,
                metadata={}
            )
            sale_items.append(sale_item)
        if next_page:
            url = "https://damsonmadder.com/" + next_page
        else:
            url = None
    return sale_items


if __name__ == "__main__":
    sale_items = damson_madder_scraper()
    for item in sale_items:
        print(item)
    
        