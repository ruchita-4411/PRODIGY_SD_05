import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import time
import random

class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.sample_products = [
            {
                'name': 'Apple MacBook Pro 13-inch',
                'price': '1299.99',
                'rating': '4.7',
                'reviews': '2,345',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Samsung Galaxy S21 Ultra',
                'price': '1199.99',
                'rating': '4.6',
                'reviews': '1,890',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Sony WH-1000XM4 Wireless Headphones',
                'price': '349.99',
                'rating': '4.8',
                'reviews': '3,567',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Nintendo Switch OLED',
                'price': '349.99',
                'rating': '4.9',
                'reviews': '4,123',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Canon EOS R5 Camera',
                'price': '3899.99',
                'rating': '4.7',
                'reviews': '890',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Dyson V15 Detect Absolute',
                'price': '699.99',
                'rating': '4.8',
                'reviews': '2,456',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Apple AirPods Pro',
                'price': '249.99',
                'rating': '4.7',
                'reviews': '5,678',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            },
            {
                'name': 'Samsung 65" QLED 4K Smart TV',
                'price': '1499.99',
                'rating': '4.6',
                'reviews': '1,234',
                'url': 'https://www.amazon.com/dp/B08N5KWB9H'
            }
        ]

    def get_product_data(self, search_query: str, num_pages: int = 1, test_mode: bool = False) -> List[Dict]:
        if test_mode:
            # Return sample products for testing
            return self.sample_products
        
        products = []
        
        for page in range(1, num_pages + 1):
            url = f'https://www.amazon.com/s?k={search_query}&page={page}'
            
            try:
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all product containers
                product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for container in product_containers:
                    try:
                        # Extract product information
                        name = container.find('span', {'class': 'a-text-normal'}).text.strip()
                        
                        # Price
                        price_element = container.find('span', {'class': 'a-price-whole'})
                        price = price_element.text.strip() if price_element else 'N/A'
                        
                        # Rating
                        rating_element = container.find('span', {'class': 'a-icon-alt'})
                        rating = rating_element.text.split(' ')[0] if rating_element else 'N/A'
                        
                        # Reviews count
                        reviews_element = container.find('span', {'class': 'a-size-base'})
                        reviews = reviews_element.text.strip() if reviews_element else '0'
                        
                        # Product URL
                        product_url = 'https://www.amazon.com' + container.find('a', {'class': 'a-link-normal'})['href']
                        
                        products.append({
                            'name': name,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'url': product_url
                        })
                        
                    except Exception as e:
                        print(f"Error extracting product data: {str(e)}")
                        continue
                
                # Add a small delay between requests to be respectful
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error fetching page {page}: {str(e)}")
                continue
        
        return products

    def save_to_csv(self, products: List[Dict], filename: str = 'products.csv'):
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False)
        return filename 