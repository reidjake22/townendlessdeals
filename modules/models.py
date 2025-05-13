from typing import TypedDict, Dict, Any, Optional, List

class SaleItem(TypedDict):
    """
    Represents a single item in a sale as returned by scrapers.
    """
    item_id: int
    item_name: str
    item_description: str
    item_price: float
    item_discounted_price: float
    item_url: str
    metadata: Dict[str, Any]

class PriceHistoryEntry(TypedDict):
    """
    Represents a single price history entry.
    """
    price: float
    discounted_price: float
    timestamp: str

class DatabaseSaleItem(SaleItem, total=False):
    """
    Represents a sale item as stored in the database.
    Extends SaleItem with database-specific fields.
    """
    site: str
    first_seen: str
    last_seen: str
    is_active: int
    price_history: List[PriceHistoryEntry]