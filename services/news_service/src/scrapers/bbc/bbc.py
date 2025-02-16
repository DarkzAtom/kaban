from bs4 import BeautifulSoup
import requests
from sqlalchemy.orm import Session
from ...database import SessionLocal
from ... import crud, schemas
from contextlib import contextmanager
import time


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
    full_desc = '\n'.join([p.text.strip() for p in paragraphs])
    print(full_desc)
    print('--------------------------------')

    shortdesc = full_desc[:50] + "..."

    author = "Moishe Finkelbaum"


    from datetime import datetime 
    date = datetime.now().strftime("%d/%m/%Y %H:%M")


    from ...article_processor import ArticleProcessor
    processor = ArticleProcessor()
    pic_shortprompt = processor.get_image_description(title, full_desc)

    print(pic_shortprompt)

    from ...image_finder import find_similar_image
    pictuple = find_similar_image(pic_shortprompt)
    picname = pictuple[0]
    print(picname)

    with get_db() as db:
        crud.create_article(
            db, 
            schemas.ArticleBase(
                title=title, 
                date=date, 
                author=author, 
                shortdesc=shortdesc, 
                fulldesc=full_desc, 
                picurl=picname
            )
        )
        crud.mark_url_as_processed(db, link)



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
        print(f"Total URLs to check: {len(hrefs)}")  # Debug print
        
        # Filter out URLs that already exist in database
        new_urls = crud.filter_new_urls(db, hrefs)
        print(f"New URLs after filtering: {len(new_urls)}")  # Debug print
        print(f"New URLs: {new_urls}")  # See what URLs we're trying to add
        
        # Add new URLs to database
        for url in new_urls:
            try:
                crud.create_url(db, url)
                print(f"Successfully added: {url}")  # Debug print
            except Exception as e:
                print(f"Error adding URL {url}: {str(e)}")  # Debug print
                db.rollback()
                continue

        return new_urls
    

def collect_and_store_all_articles_cronjob():
    """Collect all articles and store them in the database (this is the wrapper for the cronjob, for the sake of convienience)"""
    try:
        all_links = collect_all_articles_links()
        new_links = store_new_links(all_links)
        print(f"Found {len(new_links)} new articles to process, all are added to the database")
    except Exception as e:
        print(f"Error collecting and storing all articles: {str(e)}")
        raise e

def process_unprocessed_articles(limit: int = 1):
    """Process articles that haven't been scraped yet"""
    with get_db() as db:
        unprocessed_urls = crud.get_unprocessed_urls(db, limit=limit)
        
        for url_entry in unprocessed_urls:
            try:
                # Scrape the article
                scrape_bbc_news_single_article(url_entry.url)
                
                print(f"Successfully processed article: {url_entry.url}")
                time.sleep(5)
                
            except Exception as e:
                print(f"Error processing article {url_entry.url}: {str(e)}")
                continue

def bbc_main():
    """Main function to run the BBC scraper"""
    # Collect all links from BBC
    collect_and_store_all_articles_cronjob()
    
    # Process unprocessed articles
    process_unprocessed_articles(limit=5)

if __name__ == "__main__":
    bbc_main()
