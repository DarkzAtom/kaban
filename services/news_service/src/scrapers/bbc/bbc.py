from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ... import crud, schemas
from contextlib import contextmanager

@contextmanager
def get_db():
    """Database session context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def scrape_bbc_news_single_article(link: str) -> dict:
    """Scrape a single BBC article and return the data"""
    url = "https://www.bbc.com" + link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pretty_html = soup.prettify()
    with open('bbc_news_single_article.html', 'w') as f:
        f.write(pretty_html)

    # Extract the title
    title = soup.select_one('div[data-component="headline-block"] > h1').text.strip()
    print(title)
    print('--------------------------------')
    # Extract all paragraphs and join their text
    paragraphs = soup.select('div[data-component="text-block"] > p')
    main_article_text = '\n'.join([p.text.strip() for p in paragraphs])
    print(main_article_text)
    print('--------------------------------')


def collect_all_articles_links() -> list[str]:
    """Collect all article links from BBC news"""
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pretty_html = soup.prettify()
    with open('bbc_news_links_to_scrape.html', 'w') as f:
        f.write(pretty_html)

    # collect all article links
    hrefs = []
    links = soup.select('a[data-testid="internal-link"]')
    for link in links:
        href = link.get('href').strip()
        if href.startswith('/news/articles/'):
            hrefs.append(href)

    return hrefs

def store_new_links(hrefs: list[str]) -> list[str]:
    """Store new links in database and return filtered new URLs"""
    with get_db() as db:
        # Filter out URLs that already exist in database
        new_urls = crud.filter_new_urls(db, hrefs)
        
        # Add new URLs to database
        for url in new_urls:
            crud.create_url(db, url)

        return new_urls

def process_unprocessed_articles(limit: int = 1):
    """Process articles that haven't been scraped yet"""
    with get_db() as db:
        unprocessed_urls = crud.get_unprocessed_urls(db, limit=limit)
        
        for url_entry in unprocessed_urls:
            try:
                # Scrape the article
                article_data = scrape_bbc_news_single_article(url_entry.url)
                
                # Create article schema
                article_schema = schemas.ArticleBase(**article_data)
                
                # Save to database
                crud.create_article(db, article_schema)
                
                # Mark URL as processed
                crud.mark_url_as_processed(db, url_entry.id)
                
                print(f"Successfully processed article: {article_data['title']}")
                
            except Exception as e:
                print(f"Error processing article {url_entry.url}: {str(e)}")
                continue

def bbc_main():
    """Main function to run the BBC scraper"""
    # Collect all links from BBC
    all_links = collect_all_articles_links()
    
    # Store new links in database
    new_links = store_new_links(all_links)
    print(f"Found {len(new_links)} new articles to process")
    
    # Process unprocessed articles
    # process_unprocessed_articles()

if __name__ == "__main__":
    bbc_main()
