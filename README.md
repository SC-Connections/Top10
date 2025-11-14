# Top10 - Amazon Deals Site Generator

Automatically generate a beautiful Top 10 Amazon deals website using the Amazon Real-Time API.

## Features

- 🚀 Fetches live Amazon deals via RapidAPI
- 💰 Automatically adds Amazon affiliate tags to product URLs
- 🎨 Beautiful, responsive HTML design
- ⚡ Easy to use and configure

## Prerequisites

- Python 3.6+
- RapidAPI account with Amazon Real-Time API access
- Amazon Associates affiliate ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SC-Connections/Top10.git
cd Top10
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API credentials:
```bash
cp config.example.json config.json
```

Edit `config.json` with your credentials:
- `rapidapi_key`: Your RapidAPI key for Amazon Real-Time API
- `amazon_affiliate_id`: Your Amazon Associates affiliate ID
- `domain`: Amazon domain (e.g., "US")
- `node_id`: Amazon category node ID

## Usage

Run the generator:
```bash
python generate.py
```

The script will:
1. Fetch the latest deals from Amazon API
2. Generate a static HTML file with Top 10 deals
3. Save the output to `output/index.html`

Open the generated file in your browser to view your Top 10 deals site!

## Configuration

The `config.json` file contains all necessary configuration:

```json
{
  "rapidapi_key": "YOUR_RAPIDAPI_KEY",
  "rapidapi_host": "amazon-real-time-api.p.rapidapi.com",
  "amazon_affiliate_id": "YOUR_AFFILIATE_ID",
  "api_endpoint": "https://amazon-real-time-api.p.rapidapi.com/deals",
  "domain": "US",
  "node_id": "16310101"
}
```

### Node IDs

You can change the `node_id` to fetch deals from different Amazon categories:
- 16310101: Electronics
- 2619525011: Computers & Accessories
- 172282: Electronics

See Amazon's category structure for more node IDs.

## Output

The generator creates a responsive HTML page with:
- Top 10 ranked deals
- Product images
- Pricing information
- Star ratings and review counts
- Direct links to Amazon with affiliate tags

## Automation

You can automate the generation process using cron jobs or CI/CD pipelines:

```bash
# Run daily at 9 AM
0 9 * * * cd /path/to/Top10 && python generate.py
```

## License

MIT License - Feel free to use and modify as needed.

## Disclaimer

This project uses the Amazon Real-Time API and includes Amazon affiliate links. 
As an Amazon Associate, we earn from qualifying purchases. 
