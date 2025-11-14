#!/usr/bin/env python3
"""
Test suite for Top10 generator
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import generate module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate import (
    load_config,
    add_affiliate_tag,
    fetch_amazon_deals,
    generate_html,
    get_mock_deals
)


class TestTop10Generator(unittest.TestCase):
    """Test cases for the Top10 generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_config = {
            "rapidapi_key": "test_key",
            "rapidapi_host": "amazon-real-time-api.p.rapidapi.com",
            "amazon_affiliate_id": "test-affiliate-20",
            "api_endpoint": "https://amazon-real-time-api.p.rapidapi.com/deals",
            "domain": "US",
            "node_id": "16310101"
        }
        
        self.sample_deal = {
            "product_title": "Test Product",
            "product_price": "$99.99",
            "product_star_rating": "4.5",
            "product_num_ratings": "1000",
            "product_url": "https://www.amazon.com/dp/TESTID",
            "product_photo": "https://example.com/image.jpg"
        }
    
    def test_add_affiliate_tag_to_url_without_params(self):
        """Test adding affiliate tag to URL without parameters"""
        url = "https://www.amazon.com/dp/B08MQZXN1X"
        affiliate_id = "scconnec0d-20"
        result = add_affiliate_tag(url, affiliate_id)
        
        expected = "https://www.amazon.com/dp/B08MQZXN1X?tag=scconnec0d-20"
        self.assertEqual(result, expected)
    
    def test_add_affiliate_tag_to_url_with_params(self):
        """Test adding affiliate tag to URL with existing parameters"""
        url = "https://www.amazon.com/dp/B08MQZXN1X?ref=test"
        affiliate_id = "scconnec0d-20"
        result = add_affiliate_tag(url, affiliate_id)
        
        expected = "https://www.amazon.com/dp/B08MQZXN1X?ref=test&tag=scconnec0d-20"
        self.assertEqual(result, expected)
    
    def test_add_affiliate_tag_already_exists(self):
        """Test that affiliate tag is not duplicated"""
        url = "https://www.amazon.com/dp/B08MQZXN1X?tag=existing-20"
        affiliate_id = "scconnec0d-20"
        result = add_affiliate_tag(url, affiliate_id)
        
        # Should return unchanged if tag already exists
        self.assertEqual(result, url)
    
    def test_add_affiliate_tag_empty_url(self):
        """Test handling of empty URL"""
        url = ""
        affiliate_id = "scconnec0d-20"
        result = add_affiliate_tag(url, affiliate_id)
        
        self.assertEqual(result, "")
    
    def test_get_mock_deals(self):
        """Test that mock deals are returned"""
        deals = get_mock_deals()
        
        self.assertIsInstance(deals, list)
        self.assertGreater(len(deals), 0)
        self.assertIn("product_title", deals[0])
        self.assertIn("product_price", deals[0])
        self.assertIn("product_url", deals[0])
    
    def test_fetch_amazon_deals_with_mock(self):
        """Test fetching deals with mock data"""
        deals = fetch_amazon_deals(self.test_config, use_mock=True)
        
        self.assertIsInstance(deals, list)
        self.assertGreater(len(deals), 0)
    
    def test_generate_html_contains_affiliate_tags(self):
        """Test that generated HTML contains affiliate tags"""
        deals = [self.sample_deal]
        html = generate_html(deals, self.test_config)
        
        # Check that affiliate tag is in the HTML
        self.assertIn("tag=test-affiliate-20", html)
    
    def test_generate_html_contains_deal_info(self):
        """Test that generated HTML contains deal information"""
        deals = [self.sample_deal]
        html = generate_html(deals, self.test_config)
        
        # Check for product information
        self.assertIn("Test Product", html)
        self.assertIn("$99.99", html)
        self.assertIn("4.5", html)
    
    def test_generate_html_limits_to_top_10(self):
        """Test that only top 10 deals are included"""
        # Create 15 deals
        deals = [self.sample_deal.copy() for _ in range(15)]
        for i, deal in enumerate(deals):
            deal["product_title"] = f"Product {i+1}"
        
        html = generate_html(deals, self.test_config)
        
        # Should only have deals 1-10
        self.assertIn("Product 1", html)
        self.assertIn("Product 10", html)
        self.assertNotIn("Product 11", html)
    
    def test_generate_html_structure(self):
        """Test that generated HTML has proper structure"""
        deals = [self.sample_deal]
        html = generate_html(deals, self.test_config)
        
        # Check for essential HTML elements
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<html", html)
        self.assertIn("<head>", html)
        self.assertIn("<body>", html)
        self.assertIn("Top 10 Amazon Deals", html)
    
    def test_config_validation(self):
        """Test that config contains required fields"""
        required_fields = [
            "rapidapi_key",
            "rapidapi_host",
            "amazon_affiliate_id",
            "api_endpoint",
            "domain",
            "node_id"
        ]
        
        for field in required_fields:
            self.assertIn(field, self.test_config)
    
    def test_affiliate_id_format(self):
        """Test that affiliate ID has correct format"""
        affiliate_id = "scconnec0d-20"
        
        # Should end with -20 (Amazon Associates format)
        self.assertTrue(affiliate_id.endswith("-20"))
        
        # Should not contain spaces
        self.assertNotIn(" ", affiliate_id)


class TestIntegration(unittest.TestCase):
    """Integration tests"""
    
    def test_full_generation_with_mock_data(self):
        """Test complete generation flow with mock data"""
        config = {
            "rapidapi_key": "test_key",
            "rapidapi_host": "amazon-real-time-api.p.rapidapi.com",
            "amazon_affiliate_id": "scconnec0d-20",
            "api_endpoint": "https://amazon-real-time-api.p.rapidapi.com/deals",
            "domain": "US",
            "node_id": "16310101"
        }
        
        # Fetch mock deals
        deals = fetch_amazon_deals(config, use_mock=True)
        self.assertIsNotNone(deals)
        self.assertGreater(len(deals), 0)
        
        # Generate HTML
        html = generate_html(deals, config)
        self.assertIsNotNone(html)
        self.assertGreater(len(html), 1000)
        
        # Verify affiliate tags are present
        self.assertIn("tag=scconnec0d-20", html)


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    run_tests()
