# TownendlessDiscounts

TownendlessDiscounts was made as a gift for my lovely girlfriend - opensource projects are the 21st century ballad.

The idea is that you interact with a character called Delia Webster via SMS (currently).The server is a Python-based automated sale tracker and notification system for fashion websites. It monitors selected online stores for new sale items and price drops, then sends personalized SMS alerts to users using Twilio. The project is designed to help users never miss a deal on their favorite brands.

The easy next step is some persistent texts & back and forth messaging; The exciting tech idea I want to implement is trying to integrent an AI agent that can develop scrapers on the fly for new sites as folks add them. I think that it will be massively successful given that most eccomerce sites have very similar html & where powered by a third party there are massive similarities. Watch this space...

## Features

- **Automated Sale Monitoring:** Periodically scrapes sale pages of configured fashion retailers.
- **Price Drop Detection:** Tracks historical prices and notifies users of new discounts.
- **Personalized SMS Alerts:** Sends engaging, emoji-rich messages to users about deals relevant to their interests.
- **User Management:** Supports multiple users with individual preferences.
- **Extensible Scraper Architecture:** Easily add new retailers by implementing a scraper module.

## Technologies Used

- Python 3.11+
- Flask (for webhook/SMS handling)
- Twilio (SMS delivery)
- SQLite (local database for sale items and price history)
- BeautifulSoup & Requests (web scraping)
- LangChain & Groq (LLM-powered message formatting)
- dotenv (environment variable management)

## Project Structure

- `app.py` – Flask app for Twilio SMS webhook and scheduler trigger
- `main.py` – CLI entry point for manual monitoring
- `scheduler.py` – Periodic sale monitoring logic
- `modules/` – Core modules:
  - `scraping/` – Scraper implementations for each retailer
  - `checking/` – Checklist and checker logic
  - `database/` – SQLite database interface
  - `messaging/` – SMS formatting and delivery
  - `models.py` – TypedDict models for sale items

## Getting Started

### Prerequisites

- Python 3.11+
- Twilio account (for SMS)
- Groq API key (for LLM formatting)
- [See `requirements.txt`](requirements.txt)

### Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/TownendlessDiscounts.git
   cd TownendlessDiscounts
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .townenv
   source .townenv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your Twilio and Groq credentials.

5. **Initialize the database:**
   - The database will be created automatically on first run.

### Running the Project

#### Start the Flask SMS webhook (for Twilio):

```sh
python app.py
```
Or with Gunicorn (for deployment):
```sh
gunicorn app:app
```

#### Manual monitoring (CLI):

```sh
python main.py
```

### How It Works

- Users are defined in [`modules/messaging/users.json`](modules/messaging/users.json) with their interests and phone numbers.
- The scheduler periodically scrapes sale pages (see [`modules/scraping/`](modules/scraping/)), compares new items against the database, and sends SMS notifications for new deals.
- Messages are formatted using an LLM for a fun, engaging style.

## Extending

To add a new retailer:
1. Implement a scraper in `modules/scraping/<retailer>/<retailer>_scraper.py` that returns a list of [`SaleItem`](modules/models.py).
2. Add the retailer to [`modules/checking/checklist.json`](modules/checking/checklist.json).
3. Add user interests in [`modules/messaging/users.json`](modules/messaging/users.json).

## License

MIT License

---

*For questions or contributions, please open an issue
