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
# Top10 - Automated Product Review Site Generator

Automatically generate beautiful Top 10 product review sites using GitHub Actions, Amazon data via RapidAPI, and Jekyll.

## 🚀 Features

- **Automated Generation**: Create new Top10 sites with a single workflow dispatch
- **Amazon Integration**: Fetch live product data via RapidAPI
- **Affiliate Links**: Automatically adds your Amazon affiliate ID to all product links
- **Beautiful Templates**: Responsive, modern design with Jekyll
- **GitHub Actions**: Fully automated workflow with no manual setup needed

## 📋 Prerequisites

Before using this generator, you need to set up the following GitHub Secrets:

1. **RAPIDAPI_KEY**: Your RapidAPI key for accessing Amazon product data
   - Sign up at [RapidAPI](https://rapidapi.com/)
   - Subscribe to the [Amazon23 API](https://rapidapi.com/hub)
   
2. **AMAZON_AFFILIATE_ID**: Your Amazon Associates affiliate tag
   - Sign up for [Amazon Associates](https://affiliate-program.amazon.com/)
   - Get your affiliate tag/ID

### Setting Up GitHub Secrets

1. Go to your repository settings
2. Navigate to **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add both secrets:
   - Name: `RAPIDAPI_KEY`, Value: your RapidAPI key
   - Name: `AMAZON_AFFILIATE_ID`, Value: your Amazon affiliate tag

## 🎯 How to Use

### Generating a New Top10 Site

1. Go to the **Actions** tab in your repository
2. Select **Generate Top10 Site** workflow
3. Click **Run workflow**
4. Fill in the required inputs:
   - **Title**: Site title (e.g., "Best Coffee Makers 2024")
   - **Slug**: URL-friendly slug (e.g., "best-coffee-makers")
   - **Niche**: Product category (e.g., "coffee makers")
   - **Amazon Search**: Search query for Amazon API (e.g., "coffee maker")
5. Click **Run workflow**

The workflow will:
1. Fetch top 10 products from Amazon via RapidAPI
2. Generate a beautiful product review page
3. Create affiliate links with your Amazon ID
4. Commit and push the new site to your repository

### Viewing Your Sites

After the workflow completes:
- The new site will be available in the `_posts` directory
- Product data is stored in `_data` directory
- Enable GitHub Pages to view your sites online

## 📁 Repository Structure

```
Top10/
├── .github/
│   ├── workflows/
│   │   └── generate-site.yml      # GitHub Actions workflow
│   └── scripts/
│       └── fill-template.js       # Amazon data fetcher
├── _data/                         # Product data (JSON)
├── _layouts/
│   └── top10.html                # Jekyll template
├── _posts/                       # Generated sites
├── sites/                        # Future: individual site folders
├── _config.yml                   # Jekyll configuration
├── index.html                    # Site listing page
└── README.md
```

## 🎨 Template Customization

The template is located in `_layouts/top10.html`. You can customize:
- Colors and styling
- Layout and design
- Product information display
- Buttons and calls-to-action

## 🔧 Technical Details

### Workflow Steps

1. **Checkout**: Clones the repository
2. **Setup Node.js**: Installs Node.js 20
3. **Install Dependencies**: Installs mustache and axios globally
4. **Fetch Amazon Data**: Runs the data fetcher script with your API key
5. **Create Jekyll Post**: Generates the markdown post with proper frontmatter
6. **Commit & Push**: Automatically commits the new site to the repository

### Data Fetcher Script

The `fill-template.js` script:
- Connects to Amazon API via RapidAPI
- Fetches product details (title, price, rating, reviews, images)
- Transforms data to template format
- Adds affiliate links to all product URLs
- Saves data as JSON for Jekyll to consume

### Jekyll Integration

Sites are generated as Jekyll posts with:
- Custom `top10` layout
- Data file reference in frontmatter
- Automatic date-based permalinks

## 🌐 Deploying to GitHub Pages

To make your sites publicly accessible:

1. Go to **Settings** > **Pages**
2. Select **Deploy from a branch**
3. Choose **main** branch and **/ (root)** folder
4. Save and wait for deployment

Your sites will be available at: `https://[username].github.io/Top10/`

## 📝 Example

```yaml
# Workflow inputs example
Title: "Best Wireless Headphones 2024"
Slug: "best-wireless-headphones"
Niche: "wireless headphones"
Amazon Search: "wireless headphones bluetooth"
```

This generates a page with:
- Top 10 wireless headphones from Amazon
- Live pricing and ratings
- Affiliate links to purchase
- Beautiful, responsive design

## 🤝 Contributing

Feel free to fork this repository and customize it for your needs!

## 📄 License

This project is open source and available for personal and commercial use.

## ⚠️ Disclaimer

This site contains affiliate links. When you click on links and make a purchase, we may receive a commission at no extra cost to you.

## 🆘 Troubleshooting

Having issues? Check out our comprehensive [Troubleshooting Guide](TROUBLESHOOTING.md) for:
- Fixing "RAPID_KEY environment variable is required" errors
- Resolving API connection issues
- Verifying GitHub Secrets configuration
- Testing affiliate links
- And more!

Quick links:
- [Setup Guide](SETUP.md) - Detailed setup instructions
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Example Usage](EXAMPLE.md) - Usage examples
 
