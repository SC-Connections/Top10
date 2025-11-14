#!/usr/bin/env python3
"""
Top10 Site Generator
Fetches Amazon deals from RapidAPI and generates a static HTML site
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import requests


def load_config(config_path: str = "config.json") -> Dict:
    """Load configuration from JSON file"""
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        print("Please create config.json from config.example.json")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return json.load(f)


def get_mock_deals() -> List[Dict]:
    """Return mock deals data for testing"""
    return [
        {
            "product_title": "Fire TV Stick 4K Max streaming device",
            "product_price": "$54.99",
            "product_star_rating": "4.5",
            "product_num_ratings": "34,521",
            "product_url": "https://www.amazon.com/dp/B08MQZXN1X",
            "product_photo": "https://m.media-amazon.com/images/I/51wHT1UvXjL._AC_SL1000_.jpg"
        },
        {
            "product_title": "Echo Dot (5th Gen) Smart speaker with Alexa",
            "product_price": "$49.99",
            "product_star_rating": "4.7",
            "product_num_ratings": "152,304",
            "product_url": "https://www.amazon.com/dp/B09B8V1LZ3",
            "product_photo": "https://m.media-amazon.com/images/I/71Owuux5a7L._AC_SL1000_.jpg"
        },
        {
            "product_title": "Blink Mini – Compact indoor security camera",
            "product_price": "$29.99",
            "product_star_rating": "4.3",
            "product_num_ratings": "78,992",
            "product_url": "https://www.amazon.com/dp/B07X6C9RMF",
            "product_photo": "https://m.media-amazon.com/images/I/41tzXzt8hTL._AC_SL1000_.jpg"
        },
        {
            "product_title": "Kindle Paperwhite (16 GB) – Now with a larger display",
            "product_price": "$139.99",
            "product_star_rating": "4.6",
            "product_num_ratings": "45,678",
            "product_url": "https://www.amazon.com/dp/B08KTZ8249",
            "product_photo": "https://m.media-amazon.com/images/I/51QCk82iGcL._AC_SL1000_.jpg"
        },
        {
            "product_title": "Apple AirPods Pro (2nd Generation)",
            "product_price": "$199.99",
            "product_star_rating": "4.8",
            "product_num_ratings": "89,234",
            "product_url": "https://www.amazon.com/dp/B0CHWRXH8B",
            "product_photo": "https://m.media-amazon.com/images/I/61f1YfTkTDL._AC_SL1500_.jpg"
        },
        {
            "product_title": "Samsung Galaxy Buds2 Pro True Wireless Bluetooth",
            "product_price": "$149.99",
            "product_star_rating": "4.4",
            "product_num_ratings": "12,456",
            "product_url": "https://www.amazon.com/dp/B0B2SH4CN6",
            "product_photo": "https://m.media-amazon.com/images/I/61i3aWzVX-L._AC_SL1500_.jpg"
        },
        {
            "product_title": "Logitech MX Master 3S Wireless Mouse",
            "product_price": "$99.99",
            "product_star_rating": "4.7",
            "product_num_ratings": "23,890",
            "product_url": "https://www.amazon.com/dp/B09HM94VDS",
            "product_photo": "https://m.media-amazon.com/images/I/61ni3t1ryQL._AC_SL1500_.jpg"
        },
        {
            "product_title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones",
            "product_price": "$329.99",
            "product_star_rating": "4.6",
            "product_num_ratings": "18,765",
            "product_url": "https://www.amazon.com/dp/B09XS7JWHH",
            "product_photo": "https://m.media-amazon.com/images/I/51QeS073XmL._AC_SL1500_.jpg"
        },
        {
            "product_title": "Anker PowerCore 20000mAh Portable Charger",
            "product_price": "$39.99",
            "product_star_rating": "4.5",
            "product_num_ratings": "67,890",
            "product_url": "https://www.amazon.com/dp/B00X5RV14Y",
            "product_photo": "https://m.media-amazon.com/images/I/61V0HSWlVxL._AC_SL1500_.jpg"
        },
        {
            "product_title": "TP-Link AC1750 Smart WiFi Router",
            "product_price": "$69.99",
            "product_star_rating": "4.3",
            "product_num_ratings": "54,321",
            "product_url": "https://www.amazon.com/dp/B079JD7F7G",
            "product_photo": "https://m.media-amazon.com/images/I/61PpM5xD8tL._AC_SL1500_.jpg"
        }
    ]


def fetch_amazon_deals(config: Dict, use_mock: bool = False) -> Optional[List[Dict]]:
    """Fetch deals from Amazon Real-Time API via RapidAPI"""
    
    if use_mock:
        print("Using mock data for demonstration...")
        return get_mock_deals()
    
    url = config['api_endpoint']
    
    params = {
        'domain': config['domain'],
        'node_id': config['node_id']
    }
    
    headers = {
        'x-rapidapi-host': config['rapidapi_host'],
        'x-rapidapi-key': config['rapidapi_key']
    }
    
    try:
        print(f"Fetching deals from Amazon API...")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"Successfully fetched data from API")
        
        # The API response structure may vary, adjust as needed
        deals = data.get('data', {}).get('deals', [])
        
        if not deals:
            # Try alternative response structures
            deals = data.get('deals', [])
        
        if not deals and isinstance(data, list):
            deals = data
            
        return deals
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching deals: {e}")
        print("Falling back to mock data...")
        return get_mock_deals()
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None


def add_affiliate_tag(url: str, affiliate_id: str) -> str:
    """Add Amazon affiliate tag to product URL"""
    if not url:
        return url
    
    separator = '&' if '?' in url else '?'
    
    # Check if tag already exists
    if 'tag=' in url:
        return url
    
    return f"{url}{separator}tag={affiliate_id}"


def generate_html(deals: List[Dict], config: Dict) -> str:
    """Generate HTML page from deals data"""
    
    # Prepare deals with affiliate links
    processed_deals = []
    for i, deal in enumerate(deals[:10]):  # Top 10 only
        product_url = deal.get('product_url', deal.get('url', '#'))
        
        # Add affiliate tag to URL
        if product_url != '#':
            product_url = add_affiliate_tag(product_url, config['amazon_affiliate_id'])
        
        processed_deals.append({
            'rank': i + 1,
            'title': deal.get('product_title', deal.get('title', 'Product')),
            'price': deal.get('product_price', deal.get('price', 'N/A')),
            'image': deal.get('product_photo', deal.get('image', '')),
            'url': product_url,
            'rating': deal.get('product_star_rating', deal.get('rating', 'N/A')),
            'reviews': deal.get('product_num_ratings', deal.get('reviews', 'N/A'))
        })
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top 10 Amazon Deals</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            padding: 40px 20px;
        }}
        
        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .deals-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            padding: 20px;
        }}
        
        .deal-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }}
        
        .deal-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        }}
        
        .rank-badge {{
            position: absolute;
            top: 15px;
            left: 15px;
            background: #ff9900;
            color: white;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            z-index: 1;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }}
        
        .deal-image {{
            width: 100%;
            height: 250px;
            object-fit: contain;
            background: #f8f8f8;
            padding: 20px;
        }}
        
        .deal-content {{
            padding: 20px;
        }}
        
        .deal-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #232f3e;
            margin-bottom: 10px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .deal-price {{
            font-size: 1.8em;
            color: #b12704;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .deal-rating {{
            color: #666;
            margin-bottom: 15px;
            font-size: 0.9em;
        }}
        
        .deal-button {{
            display: block;
            width: 100%;
            padding: 12px;
            background: #ff9900;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.3s;
        }}
        
        .deal-button:hover {{
            background: #e88900;
        }}
        
        footer {{
            text-align: center;
            color: white;
            padding: 40px 20px;
            opacity: 0.9;
        }}
        
        .timestamp {{
            font-size: 0.9em;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏆 Top 10 Amazon Deals</h1>
            <p class="subtitle">Best deals curated just for you</p>
        </header>
        
        <div class="deals-grid">
"""
    
    # Add deals
    for deal in processed_deals:
        html += f"""
            <div class="deal-card">
                <div class="rank-badge">#{deal['rank']}</div>
                <img src="{deal['image']}" alt="{deal['title']}" class="deal-image" onerror="this.src='https://via.placeholder.com/300x250?text=No+Image'">
                <div class="deal-content">
                    <h3 class="deal-title">{deal['title']}</h3>
                    <div class="deal-price">{deal['price']}</div>
                    <div class="deal-rating">⭐ {deal['rating']} ({deal['reviews']} reviews)</div>
                    <a href="{deal['url']}" target="_blank" class="deal-button">View Deal on Amazon</a>
                </div>
            </div>
"""
    
    html += f"""
        </div>
        
        <footer>
            <p>Deals fetched from Amazon via RapidAPI</p>
            <p class="timestamp">Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="font-size: 0.8em; margin-top: 20px;">
                As an Amazon Associate, we earn from qualifying purchases.
            </p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html


def main():
    """Main function to run the generator"""
    print("=" * 60)
    print("Top10 Site Generator")
    print("=" * 60)
    print()
    
    # Load configuration
    config = load_config()
    print(f"✓ Configuration loaded")
    print(f"  - Amazon Affiliate ID: {config['amazon_affiliate_id']}")
    print(f"  - API Endpoint: {config['api_endpoint']}")
    print()
    
    # Fetch deals
    deals = fetch_amazon_deals(config)
    
    if not deals:
        print("✗ Failed to fetch deals or no deals available")
        sys.exit(1)
    
    print(f"✓ Fetched {len(deals)} deals")
    print()
    
    # Generate HTML
    html_content = generate_html(deals, config)
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write HTML file
    output_file = os.path.join(output_dir, "index.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Generated HTML file: {output_file}")
    print()
    print("=" * 60)
    print("Generation complete! Open the file in your browser:")
    print(f"  file://{os.path.abspath(output_file)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
