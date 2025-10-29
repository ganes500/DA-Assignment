import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from urllib.parse import quote
import re
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EcommerceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
        })

    def delay(self):
        """Add random delay between requests to be respectful to servers"""
        time.sleep(random.uniform(1, 3))

    def clean_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        # Remove currency symbols and commas, then extract numbers
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        if price_match:
            return float(price_match.group())
        return None

    def clean_rating(self, rating_text):
        """Extract numeric rating from text"""
        if not rating_text:
            return None
        rating_match = re.search(r'[\d\.]+', rating_text)
        if rating_match:
            return float(rating_match.group())
        return None


class AmazonScraper(EcommerceScraper):
    def search_products(self, query, max_results=10):
        """Search products on Amazon"""
        try:
            base_url = "https://www.amazon.in/s"
            params = {
                'k': query,
                'ref': 'nb_sb_noss'
            }

            response = self.session.get(base_url, params=params)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products = []

            # Find product containers - Amazon has multiple possible selectors
            product_selectors = [
                'div[data-component-type="s-search-result"]',
                '.s-result-item',
                '.s-main-slot .s-result-item'
            ]

            product_elements = []
            for selector in product_selectors:
                product_elements = soup.select(selector)
                if product_elements:
                    break

            for product in product_elements[:max_results]:
                try:
                    # Product name
                    name_elem = product.select_one('h2 a span') or product.select_one('.a-text-normal')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"

                    # Price
                    price_elem = product.select_one('.a-price-whole')
                    price = self.clean_price(price_elem.get_text(strip=True)) if price_elem else None

                    # Rating
                    rating_elem = product.select_one('.a-icon-alt')
                    rating = self.clean_rating(rating_elem.get_text(strip=True)) if rating_elem else None

                    # Reviews count
                    reviews_elem = product.select_one('.a-size-base.s-underline-text')
                    reviews = reviews_elem.get_text(strip=True) if reviews_elem else "0"

                    # Product URL
                    link_elem = product.select_one('h2 a')
                    product_url = "https://www.amazon.in" + link_elem['href'] if link_elem else "N/A"

                    if name != "N/A" and price:
                        products.append({
                            'website': 'Amazon',
                            'name': name,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'url': product_url,
                            'search_query': query
                        })

                except Exception as e:
                    logger.warning(f"Error parsing Amazon product: {e}")
                    continue

            self.delay()
            return products

        except Exception as e:
            logger.error(f"Error searching Amazon: {e}")
            return []


class FlipkartScraper(EcommerceScraper):
    def search_products(self, query, max_results=10):
        """Search products on Flipkart"""
        try:
            encoded_query = quote(query)
            url = f"https://www.flipkart.com/search?q={encoded_query}"

            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products = []

            # Flipkart product containers
            product_elements = soup.select('div[data-id]')

            for product in product_elements[:max_results]:
                try:
                    # Product name
                    name_elem = product.select_one('a[title]') or product.select_one('._4rR01T') or product.select_one(
                        '.s1Q9rs')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"

                    # Price
                    price_elem = product.select_one('._30jeq3') or product.select_one('._1_WHN1')
                    price = self.clean_price(price_elem.get_text(strip=True)) if price_elem else None

                    # Rating
                    rating_elem = product.select_one('._3LWZlK') or product.select_one('.fa-star-o')
                    rating = self.clean_rating(rating_elem.get_text(strip=True)) if rating_elem else None

                    # Reviews count
                    reviews_elem = product.select_one('._2_R_DZ') or product.select_one('span._2_R_DZ')
                    reviews = reviews_elem.get_text(strip=True) if reviews_elem else "0"

                    # Product URL
                    link_elem = product.select_one('a._1fQZEK') or product.select_one('a.s1Q9rs') or product.select_one(
                        'a[href*="/p/"]')
                    product_url = "https://www.flipkart.com" + link_elem['href'] if link_elem else "N/A"

                    if name != "N/A" and price:
                        products.append({
                            'website': 'Flipkart',
                            'name': name,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'url': product_url,
                            'search_query': query
                        })

                except Exception as e:
                    logger.warning(f"Error parsing Flipkart product: {e}")
                    continue

            self.delay()
            return products

        except Exception as e:
            logger.error(f"Error searching Flipkart: {e}")
            return []


class ChromaScraper(EcommerceScraper):
    def search_products(self, query, max_results=10):
        """Search products on Chroma"""
        try:
            encoded_query = quote(query)
            url = f"https://www.chromastore.com/search?type=product&q={encoded_query}"

            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products = []

            # Chroma product containers
            product_elements = soup.select('.product-item') or soup.select('.grid__item')

            for product in product_elements[:max_results]:
                try:
                    # Product name
                    name_elem = product.select_one('.product-item__title') or product.select_one('.card__heading')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"

                    # Price
                    price_elem = product.select_one('.money') or product.select_one('.price-item')
                    price = self.clean_price(price_elem.get_text(strip=True)) if price_elem else None

                    # Rating (Chroma might not have ratings on search page)
                    rating = None
                    reviews = "N/A"

                    # Product URL
                    link_elem = product.select_one('a') or product.select_one('.full-unstyled-link')
                    product_url = "https://www.chromastore.com" + link_elem['href'] if link_elem else "N/A"

                    if name != "N/A" and price:
                        products.append({
                            'website': 'Chroma',
                            'name': name,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'url': product_url,
                            'search_query': query
                        })

                except Exception as e:
                    logger.warning(f"Error parsing Chroma product: {e}")
                    continue

            self.delay()
            return products

        except Exception as e:
            logger.error(f"Error searching Chroma: {e}")
            return []


class RelianceDigitalScraper(EcommerceScraper):
    def search_products(self, query, max_results=10):
        """Search products on Reliance Digital"""
        try:
            encoded_query = quote(query)
            url = f"https://www.reliancedigital.in/search?q={encoded_query}"

            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            products = []

            # Reliance Digital product containers
            product_elements = soup.select('.sp.grid') or soup.select('.product__list--item')

            for product in product_elements[:max_results]:
                try:
                    # Product name
                    name_elem = product.select_one('.sp__name') or product.select_one('.plp-prod-title')
                    name = name_elem.get_text(strip=True) if name_elem else "N/A"

                    # Price
                    price_elem = product.select_one('.TextWeb__Text-sc-1cyx778-0') or product.select_one(
                        '.plp-price-details')
                    price = self.clean_price(price_elem.get_text(strip=True)) if price_elem else None

                    # Rating
                    rating_elem = product.select_one('.starbg') or product.select_one('.plp-ratings-reviews')
                    rating = self.clean_rating(rating_elem.get_text(strip=True)) if rating_elem else None

                    reviews = "N/A"  # Reliance Digital might not show reviews count on search page

                    # Product URL
                    link_elem = product.select_one('a') or product.select_one('.sp__productLink')
                    product_url = "https://www.reliancedigital.in" + link_elem['href'] if link_elem else "N/A"

                    if name != "N/A" and price:
                        products.append({
                            'website': 'Reliance Digital',
                            'name': name,
                            'price': price,
                            'rating': rating,
                            'reviews': reviews,
                            'url': product_url,
                            'search_query': query
                        })

                except Exception as e:
                    logger.warning(f"Error parsing Reliance Digital product: {e}")
                    continue

            self.delay()
            return products

        except Exception as e:
            logger.error(f"Error searching Reliance Digital: {e}")
            return []


class ProductSearchManager:
    def __init__(self):
        self.scrapers = {
            'amazon': AmazonScraper(),
            'flipkart': FlipkartScraper(),
            'chroma': ChromaScraper(),
            'reliance': RelianceDigitalScraper()
        }

    def search_all_websites(self, query, max_results_per_site=10, websites=None):
        """Search products across all specified websites"""
        if websites is None:
            websites = ['amazon', 'flipkart', 'chroma', 'reliance']

        all_products = []

        for website in websites:
            if website.lower() in self.scrapers:
                logger.info(f"Searching {website} for: {query}")
                try:
                    products = self.scrapers[website.lower()].search_products(query, max_results_per_site)
                    all_products.extend(products)
                    logger.info(f"Found {len(products)} products from {website}")
                except Exception as e:
                    logger.error(f"Failed to search {website}: {e}")
            else:
                logger.warning(f"Unknown website: {website}")

        return all_products

    def save_to_excel(self, products, filename=None):
        """Save products to Excel file"""
        if not products:
            logger.warning("No products to save")
            return False

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"product_search_results_{timestamp}.xlsx"

        try:
            df = pd.DataFrame(products)

            # Reorder columns for better readability
            column_order = ['website', 'name', 'price', 'rating', 'reviews', 'url', 'search_query']
            df = df.reindex(columns=column_order)

            # Create directory if it doesn't exist
            os.makedirs('search_results', exist_ok=True)
            filepath = os.path.join('search_results', filename)

            df.to_excel(filepath, index=False, engine='openpyxl')
            logger.info(f"Results saved to: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving to Excel: {e}")
            return False


def main():
    """Main function to run the web scraping application"""
    print("=" * 60)
    print("        E-COMMERCE PRODUCT SEARCH SCRAPER")
    print("=" * 60)

    manager = ProductSearchManager()

    while True:
        print("\nOptions:")
        print("1. Search products")
        print("2. Exit")

        choice = input("\nEnter your choice (1-2): ").strip()

        if choice == '1':
            # Get search query from user
            query = input("\nEnter product to search: ").strip()
            if not query:
                print("Please enter a valid search query.")
                continue

            # Get maximum results
            try:
                max_results = int(input("Enter maximum results per website (default 10): ") or "10")
            except ValueError:
                max_results = 10

            # Select websites
            print("\nAvailable websites:")
            print("1. Amazon")
            print("2. Flipkart")
            print("3. Chroma")
            print("4. Reliance Digital")
            print("5. All websites")

            website_choice = input("Select websites (1-5, comma-separated): ").strip()

            website_map = {
                '1': 'amazon',
                '2': 'flipkart',
                '3': 'chroma',
                '4': 'reliance'
            }

            if website_choice == '5':
                websites = ['amazon', 'flipkart', 'chroma', 'reliance']
            else:
                websites = []
                for choice in website_choice.split(','):
                    if choice.strip() in website_map:
                        websites.append(website_map[choice.strip()])

                if not websites:
                    print("No valid websites selected. Using all websites.")
                    websites = ['amazon', 'flipkart', 'chroma', 'reliance']

            print(f"\nSearching for '{query}' on {', '.join(websites)}...")

            # Perform search
            products = manager.search_all_websites(
                query=query,
                max_results_per_site=max_results,
                websites=websites
            )

            if products:
                # Save results
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"products_{query.replace(' ', '_')}_{timestamp}.xlsx"

                if manager.save_to_excel(products, filename):
                    print(f"\n✓ Successfully saved {len(products)} products to 'search_results/{filename}'")

                    # Display summary
                    df = pd.DataFrame(products)
                    print("\nSearch Summary:")
                    print(f"Total products found: {len(products)}")
                    for website in df['website'].unique():
                        count = len(df[df['website'] == website])
                        avg_price = df[df['website'] == website]['price'].mean()
                        print(f"  {website}: {count} products (avg price: ₹{avg_price:.2f})")
                else:
                    print("✗ Failed to save results.")
            else:
                print("✗ No products found for the given search.")

        elif choice == '2':
            print("Thank you for using the E-commerce Product Search Scraper!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
    except ImportError as e:
        print("Please install required packages:")
        print("pip install requests beautifulsoup4 pandas openpyxl")
        exit(1)

    main()