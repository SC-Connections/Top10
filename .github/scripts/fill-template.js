#!/usr/bin/env node

/**
 * Fetch Amazon product data via RapidAPI and fill template
 * Uses environment variables for configuration
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Configuration from environment variables
const RAPID_KEY = process.env.RAPID_KEY;
const AMAZON_AFFILIATE_ID = process.env.AMAZON_AFFILIATE_ID || 'your-affiliate-id';
const TITLE = process.env.TITLE || 'Top 10 Products';
const SLUG = process.env.SLUG || 'top-10-products';
const NICHE = process.env.NICHE || 'products';
const SEARCH_QUERY = process.env.SEARCH_QUERY || '';

if (!RAPID_KEY) {
  console.error('╔══════════════════════════════════════════════════════════════════╗');
  console.error('║  ERROR: Missing RapidAPI Key                                     ║');
  console.error('╚══════════════════════════════════════════════════════════════════╝');
  console.error('');
  console.error('The RAPID_KEY environment variable is empty or not set.');
  console.error('');
  console.error('This usually means your GitHub secret is not configured correctly.');
  console.error('');
  console.error('To fix this:');
  console.error('  1. Go to: Settings > Secrets and variables > Actions');
  console.error('  2. Create a new repository secret named: RAPIDAPI_KEY');
  console.error('     (Note: Use exactly this name - it\'s case-sensitive!)');
  console.error('  3. Set the value to your RapidAPI key');
  console.error('');
  console.error('Alternative secret names that will also work:');
  console.error('  - RAPIDAPI_KEY (recommended)');
  console.error('  - RAPID_API_KEY');
  console.error('  - RAPID_KEY');
  console.error('  - RAPIDAPIKEY');
  console.error('');
  console.error('For detailed setup instructions, see: SETUP.md');
  console.error('');
  process.exit(1);
}

if (!process.env.AMAZON_AFFILIATE_ID) {
  console.warn('╔══════════════════════════════════════════════════════════════════╗');
  console.warn('║  WARNING: Amazon Affiliate ID not set                           ║');
  console.warn('╚══════════════════════════════════════════════════════════════════╝');
  console.warn('');
  console.warn('Using default affiliate ID. You won\'t earn commissions!');
  console.warn('');
  console.warn('To fix this:');
  console.warn('  1. Go to: Settings > Secrets and variables > Actions');
  console.warn('  2. Create a new repository secret named: AMAZON_AFFILIATE_ID');
  console.warn('  3. Set the value to your Amazon Associates tracking ID');
  console.warn('');
  console.warn('For setup instructions, see: SETUP.md');
  console.warn('');
}

/**
 * Fetch Amazon products using RapidAPI
 */
async function fetchAmazonProducts() {
  try {
    console.log(`Fetching Amazon products for: ${SEARCH_QUERY}`);
    
    const options = {
      method: 'GET',
      url: 'https://amazon23.p.rapidapi.com/product-search',
      params: {
        query: SEARCH_QUERY,
        country: 'US'
      },
      headers: {
        'X-RapidAPI-Key': RAPID_KEY,
        'X-RapidAPI-Host': 'amazon23.p.rapidapi.com'
      }
    };

    const response = await axios.request(options);
    
    if (response.data && response.data.result) {
      return response.data.result.slice(0, 10); // Get top 10 results
    } else {
      console.error('Unexpected API response structure');
      return [];
    }
  } catch (error) {
    console.error('Error fetching Amazon products:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    // Return mock data for testing/demo purposes
    return generateMockData();
  }
}

/**
 * Generate mock data for testing when API is unavailable
 */
function generateMockData() {
  console.log('Using mock data for demonstration');
  const mockProducts = [];
  
  for (let i = 1; i <= 10; i++) {
    mockProducts.push({
      title: `${NICHE} Product #${i}`,
      asin: `B00${i.toString().padStart(7, '0')}`,
      price: {
        current_price: (Math.random() * 100 + 20).toFixed(2),
        currency: 'USD'
      },
      rating: (Math.random() * 1 + 4).toFixed(1),
      reviews_count: Math.floor(Math.random() * 5000 + 100),
      thumbnail: `https://via.placeholder.com/300x300?text=Product+${i}`,
      url: `https://www.amazon.com/dp/B00${i.toString().padStart(7, '0')}`
    });
  }
  
  return mockProducts;
}

/**
 * Transform product data to our template format
 */
function transformProducts(products) {
  return products.map((product, index) => {
    // Extract ASIN from URL if not directly available
    let asin = product.asin;
    if (!asin && product.url) {
      const match = product.url.match(/\/dp\/([A-Z0-9]{10})/);
      asin = match ? match[1] : '';
    }
    
    // Build affiliate link
    const baseUrl = product.url || `https://www.amazon.com/dp/${asin}`;
    const affiliateUrl = `${baseUrl}${baseUrl.includes('?') ? '&' : '?'}tag=${AMAZON_AFFILIATE_ID}`;
    
    return {
      rank: index + 1,
      title: product.title || `Product ${index + 1}`,
      asin: asin,
      price: product.price?.current_price || product.price?.value || 'N/A',
      currency: product.price?.currency || 'USD',
      rating: product.rating || product.stars || 'N/A',
      reviews: product.reviews_count || product.total_reviews || 0,
      image: product.thumbnail || product.product_photo || 'https://via.placeholder.com/300x300',
      url: affiliateUrl,
      features: product.product_details || product.features || [],
      description: product.product_description || ''
    };
  });
}

/**
 * Main execution
 */
async function main() {
  console.log('Starting Amazon data fetch...');
  console.log(`Title: ${TITLE}`);
  console.log(`Slug: ${SLUG}`);
  console.log(`Niche: ${NICHE}`);
  
  // Fetch products
  const products = await fetchAmazonProducts();
  console.log(`Fetched ${products.length} products`);
  
  // Transform to template format
  const transformedProducts = transformProducts(products);
  
  // Create output data structure
  const outputData = {
    title: TITLE,
    slug: SLUG,
    niche: NICHE,
    generated_at: new Date().toISOString(),
    affiliate_id: AMAZON_AFFILIATE_ID,
    products: transformedProducts
  };
  
  // Ensure _data directory exists
  const dataDir = path.join(process.cwd(), '_data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  // Write to filled.json
  const outputPath = path.join(dataDir, 'filled.json');
  fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
  
  console.log(`Data written to ${outputPath}`);
  console.log('Success!');
}

// Run the script
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
