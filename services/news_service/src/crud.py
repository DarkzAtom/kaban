from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_article(db: Session, article_id: int) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_article_by_title(db: Session, title: str) -> Optional[models.Article]:
    return db.query(models.Article).filter(models.Article.id == title).first()

def get_articles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Article]:
    return db.query(models.Article).offset(skip).limit(limit).all()

def create_article(db: Session, article: schemas.ArticleBase) -> models.Article:
    db_article = models.Article(
        title=article.title,
        date=article.date,
        author=article.author,
        shortdesc=article.shortdesc,
        fulldesc=article.fulldesc,
        picurl=article.picurl
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_url(db: Session, url: str) -> Optional[models.BbcUrl]:
    """Check if URL already exists in database"""
    return db.query(models.BbcUrl).filter(models.BbcUrl.url == url).first()

def create_url(db: Session, url: str) -> models.BbcUrl:
    """Create new URL entry if it doesn't exist"""
    db_url = models.BbcUrl(url=url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_unprocessed_urls(db: Session, limit: int = 10) -> List[models.BbcUrl]:
    """Get URLs that haven't been processed yet, starting with the oldest ones"""
    return db.query(models.BbcUrl)\
        .filter(models.BbcUrl.processed == False)\
        .order_by(models.BbcUrl.id.asc())\
        .limit(limit)\
        .all()

def mark_url_as_processed(db: Session, url_href: str) -> models.BbcUrl:
    """Mark URL as processed after article has been created"""
    db_url = db.query(models.BbcUrl).filter(models.BbcUrl.url == url_href).first()
    if db_url:
        db_url.processed = True
        db.commit()
        db.refresh(db_url)
    return db_url

def filter_new_urls(db: Session, urls: List[str]) -> List[str]:
    """Filter out URLs that already exist in database"""
    existing_urls = set(
        url[0] for url in 
        db.query(models.BbcUrl.url).all()
    )
    return [url for url in urls if url not in existing_urls]

def get_all_news(db: Session) -> List[models.Article]:
    return db.query(models.Article).all()