# API Integration Documentation

## Overview

This document describes how the Top10 generator integrates with the Amazon Real-Time API via RapidAPI.

## API Configuration

### RapidAPI Credentials

The generator is configured with the following credentials:

- **RapidAPI Key**: `2152f2de12mshc2f77638455de9cp1db88cjsn0926e2e91005`
- **RapidAPI Host**: `amazon-real-time-api.p.rapidapi.com`
- **Amazon Affiliate ID**: `scconnec0d-20`

These credentials are stored in `config.json` (not committed to version control).

### API Endpoint

```
GET https://amazon-real-time-api.p.rapidapi.com/deals
```

**Parameters:**
- `domain`: Amazon marketplace domain (e.g., "US")
- `node_id`: Amazon category node ID (e.g., "16310101" for Electronics)

**Headers:**
- `x-rapidapi-host`: amazon-real-time-api.p.rapidapi.com
- `x-rapidapi-key`: Your RapidAPI key

## API Request Example

```bash
curl --request GET \
  --url 'https://amazon-real-time-api.p.rapidapi.com/deals?domain=US&node_id=16310101' \
  --header 'x-rapidapi-host: amazon-real-time-api.p.rapidapi.com' \
  --header 'x-rapidapi-key: 2152f2de12mshc2f77638455de9cp1db88cjsn0926e2e91005'
```

## Response Format

The API returns a JSON response with deals information. The generator handles multiple response formats:

```json
{
  "data": {
    "deals": [
      {
        "product_title": "Product Name",
        "product_price": "$99.99",
        "product_star_rating": "4.5",
        "product_num_ratings": "1000",
        "product_url": "https://www.amazon.com/dp/PRODUCTID",
        "product_photo": "https://image-url.jpg"
      }
    ]
  }
}
```

Or simplified format:

```json
{
  "deals": [ ... ]
}
```

Or direct array:

```json
[ ... ]
```

## Affiliate Link Integration

All Amazon product URLs are automatically enhanced with the affiliate tag:

**Original URL:**
```
https://www.amazon.com/dp/B08MQZXN1X
```

**Enhanced URL:**
```
https://www.amazon.com/dp/B08MQZXN1X?tag=scconnec0d-20
```

The `add_affiliate_tag()` function in `generate.py` handles:
- URLs without existing query parameters
- URLs with existing query parameters
- Avoiding duplicate tags if one already exists

## Fallback Mechanism

If the API is unavailable (network issues, rate limiting, etc.), the generator automatically falls back to mock data to ensure the site can still be generated for testing purposes.

## Error Handling

The generator handles various error scenarios:

1. **Network Errors**: Falls back to mock data
2. **Invalid JSON**: Logs error and returns None
3. **Missing Configuration**: Exits with error message
4. **Empty Response**: Falls back to mock data

## Rate Limits

Be aware of RapidAPI rate limits for the Amazon Real-Time API. Check your RapidAPI dashboard for your plan's limits.

## Amazon Associates Compliance

The generated site includes:
- Affiliate links with proper tag format (`tag=scconnec0d-20`)
- Disclosure statement: "As an Amazon Associate, we earn from qualifying purchases"
- Direct links to Amazon product pages

## Category Node IDs

Common Amazon category node IDs you can use:

- `16310101`: Electronics
- `2619525011`: Computers & Accessories  
- `172282`: Electronics (alternative)
- `2335752011`: Cell Phones & Accessories
- `1064954`: Office Products
- `165793011`: Home & Kitchen

To find more node IDs, browse Amazon categories and inspect the URL parameters.

## Security Considerations

- API keys are stored in `config.json` which is excluded from version control via `.gitignore`
- Always use HTTPS for API requests
- Never commit `config.json` to public repositories
- Use `config.example.json` as a template for others

## Testing

The generator includes mock data that mirrors the actual API response structure, allowing you to test the site generation without making API calls.

To force use of mock data:
```python
deals = fetch_amazon_deals(config, use_mock=True)
```

## Monitoring

Monitor your API usage through:
1. RapidAPI Dashboard: Track requests, rate limits, and errors
2. Generator logs: The script outputs status messages for each API call
