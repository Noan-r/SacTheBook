#!/usr/bin/env python3
"""
Test script to verify chess piece images are loading correctly
"""

import requests
import sys

def test_image_url(url):
    """Test if an image URL is accessible"""
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            print(f"❌ {url} - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {url} - Error: {e}")
        return False

def main():
    print("🧪 Testing chess piece images...")
    
    # Test CDN images
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    cdn_urls = [f"https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png" for piece in pieces]
    
    print("\n📡 Testing CDN images:")
    success_count = 0
    for url in cdn_urls:
        if test_image_url(url):
            print(f"✅ {url}")
            success_count += 1
        else:
            print(f"❌ {url}")
    
    print(f"\n📊 Results: {success_count}/{len(cdn_urls)} CDN images accessible")
    
    if success_count == len(cdn_urls):
        print("🎉 All CDN images are accessible!")
        return 0
    else:
        print("⚠️  Some images are not accessible")
        return 1

if __name__ == "__main__":
    sys.exit(main())
