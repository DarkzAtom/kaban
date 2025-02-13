from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    date: str
    author: str
    shortdesc: str
    fulldesc: str
    picurl: str

class Article(ArticleBase):
    id: int

    class Config:
        from_attributes = True

class BbcUrlBase(BaseModel):
    url: str
    processed: bool = False

class BbcUrl(BbcUrlBase):
    id: int

    class Config:
        from_attributes = True