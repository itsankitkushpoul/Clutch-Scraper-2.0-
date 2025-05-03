# Clutch Scraper API

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install playwright
   playwright install
   ```

3. Copy `.env.example` to `.env` and adjust values.

## Running Locally

```bash
uvicorn app.main:app --reload
```

## Environment Variables

- `HEADLESS`: `true` or `false`
- `USE_AGENT`: `true` or `false`
- `HOST`, `PORT`, `LOG_LEVEL`
- `ALLOW_ORIGINS`, `ALLOW_METHODS`, `ALLOW_HEADERS`

## API Endpoints

### POST `/scrape`

**Request body**
```json
{
  "base_url": "https://clutch.co/agencies/digital-marketing",
  "total_pages": 3
}
```

**Response**
```json
{
  "message": "Scraped X companies",
  "data": [
    { "sno": 1, "name": "...", "website": "...", "location": "..." },
    ...
  ]
}
```
