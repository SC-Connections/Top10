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
const NODE_ID = process.env.NODE_ID || '';  // Allow custom node_id override

/**
 * Map common product categories/niches to Amazon node IDs
 * Can be overridden by NODE_ID environment variable
 */
function getCategoryNodeId(niche, searchQuery) {
  // If NODE_ID is explicitly set, use it
  if (NODE_ID) {
    return NODE_ID;
  }
  
  // Map common keywords to category node IDs
  const nicheKeywords = (niche + ' ' + searchQuery).toLowerCase();
  
  if (nicheKeywords.includes('electronics') || nicheKeywords.includes('gadget')) {
    return '16310101';  // Electronics
  } else if (nicheKeywords.includes('computer') || nicheKeywords.includes('laptop') || nicheKeywords.includes('pc')) {
    return '2619525011';  // Computers & Accessories
  } else if (nicheKeywords.includes('phone') || nicheKeywords.includes('mobile') || nicheKeywords.includes('cell')) {
    return '2335752011';  // Cell Phones & Accessories
  } else if (nicheKeywords.includes('office') || nicheKeywords.includes('desk') || nicheKeywords.includes('stationery')) {
    return '1064954';  // Office Products
  } else if (nicheKeywords.includes('home') || nicheKeywords.includes('kitchen') || nicheKeywords.includes('cooking')) {
    return '165793011';  // Home & Kitchen
  } else {
    // Default to Electronics for general products
    return '16310101';
  }
}

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
    const nodeId = getCategoryNodeId(NICHE, SEARCH_QUERY);
    console.log(`Fetching Amazon deals for category node: ${nodeId}`);
    console.log(`  Niche: ${NICHE}`);
    console.log(`  Search context: ${SEARCH_QUERY}`);
    
    const options = {
      method: 'GET',
      url: 'https://amazon-real-time-api.p.rapidapi.com/deals',
      params: {
        domain: 'US',
        node_id: nodeId
      },
      headers: {
        'X-RapidAPI-Key': RAPID_KEY,
        'X-RapidAPI-Host': 'amazon-real-time-api.p.rapidapi.com'
      }
    };

    const response = await axios.request(options);
    
    // Handle multiple possible response formats from Amazon Real-Time API
    let deals = null;
    
    if (response.data) {
      // Format 1: { data: { deals: [...] } }
      if (response.data.data && response.data.data.deals) {
        deals = response.data.data.deals;
      }
      // Format 2: { deals: [...] }
      else if (response.data.deals) {
        deals = response.data.deals;
      }
      // Format 3: Direct array [...]
      else if (Array.isArray(response.data)) {
        deals = response.data;
      }
    }
    
    if (deals && Array.isArray(deals) && deals.length > 0) {
      return deals.slice(0, 10); // Get top 10 results
    } else {
      console.error('Unexpected API response structure or empty results');
      console.error('Response data:', JSON.stringify(response.data, null, 2));
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
    let asin = product.asin || product.product_asin;
    if (!asin && (product.url || product.product_url)) {
      const url = product.url || product.product_url;
      const match = url.match(/\/dp\/([A-Z0-9]{10})/);
      asin = match ? match[1] : '';
    }
    
    // Build affiliate link
    const productUrl = product.url || product.product_url || `https://www.amazon.com/dp/${asin}`;
    const affiliateUrl = `${productUrl}${productUrl.includes('?') ? '&' : '?'}tag=${AMAZON_AFFILIATE_ID}`;
    
    // Extract price - handle both old and new API formats
    let price = 'N/A';
    if (product.product_price) {
      // New API: "$99.99" format
      price = product.product_price;
    } else if (product.price?.current_price) {
      // Old API: { current_price: "99.99" } format
      price = product.price.current_price;
    } else if (product.price?.value) {
      price = product.price.value;
    }
    
    // Extract rating - handle both formats
    const rating = product.product_star_rating || product.rating || product.stars || 'N/A';
    
    // Extract reviews count - handle both formats
    const reviews = product.product_num_ratings || product.reviews_count || product.total_reviews || 0;
    
    // Extract title - handle both formats
    const title = product.product_title || product.title || `Product ${index + 1}`;
    
    // Extract image - handle both formats
    const image = product.product_photo || product.thumbnail || product.product_photo || 'https://via.placeholder.com/300x300';
    
    return {
      rank: index + 1,
      title: title,
      asin: asin,
      price: price,
      currency: product.price?.currency || 'USD',
      rating: rating,
      reviews: reviews,
      image: image,
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
