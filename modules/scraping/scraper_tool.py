from .damson_madder.damson_madder_scraper import damson_madder_scraper
from ..models import SaleItem


def scrape_sale_page(org: str)-> list[SaleItem]:
    """
    Scrape the sale page of a given organization.
    
    Args:
        org (str): The name of the organization to scrape.
    
    Returns:
        list[SaleItem]: A list of SaleItem objects containing the scraped data.
    """
    print(f"Scraping sale page for {org}...")
    if org == "damson_madder":
        print("Scraping Damson Madder sale page...")
        data = damson_madder_scraper()
    return data
