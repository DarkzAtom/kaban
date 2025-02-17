import { useEffect, useState } from 'react';
import './HomePage.css';
import { newsApi } from '../../api';

// Mock data





// const featuredNews = {
//   title: "Breaking: Major Scientific Discovery Announced",
//   description:
//     "Scientists have made a groundbreaking discovery that could revolutionize our understanding of the universe.",
//   image: "https://placehold.co/800x400",
//   date: "2025-02-10",
// }

// const recentNews = [
//   {
//     title: "Tech Giant Unveils New AI-Powered Device",
//     description: "The latest innovation promises to transform daily life with advanced artificial intelligence.",
//     image: "https://placehold.co/300x200",
//     date: "2025-02-09",
//   },
//   {
//     title: "Global Climate Summit Reaches Landmark Agreement",
//     description: "World leaders commit to ambitious targets in the fight against climate change.",
//     image: "https://placehold.co/300x200",
//     date: "2025-02-08",
//   },
//   {
//     title: "Sports: Underdog Team Wins Championship in Stunning Upset",
//     description: "In a David vs. Goliath story, the underdogs emerged victorious against all odds.",
//     image: "https://placehold.co/300x200",
//     date: "2025-02-07",
//   },
//   {
//     title: "Sports: Underdog Team Wins Championship in Stunning Upset",
//     description: "In a David vs. Goliath story, the underdogs emerged victorious against all odds.",
//     image: "https://placehold.co/300x200",
//     date: "2025-02-07",
//   },
// ]

// Add this type definition
type NewsArticle = {
  title: string;
  date: string;
  author: string;
  shortdesc: string;
  fulldesc: string;
  picurl: string;
};

function HomePage() {
  // All state declarations at the top level of the component
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [featuredNews, setFeaturedNews] = useState({
    title: "",
    date: "",
    author: "",
    shortdesc: "",
    fulldesc: "",
    picurl: ""
  });
  const [recentNews, setRecentNews] = useState<Array<{
    title: string,
    date: string,
    author: string,
    shortdesc: string,
    fulldesc: string,
    picurl: string
  }>>([]);

  useEffect(() => {
    document.title = 'NewsHub - Your Daily News Source';
    
    const fetchNews = async () => {
      const response = await newsApi.get('/news/all');
      console.log(response.data);

      if (response.data && response.data.length > 0) {
        // Sort articles by date in descending order
        const sortedArticles = [...response.data].sort((a, b) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        ).reverse();

        // Set the most recent article as featured
        const latestArticle = sortedArticles[0];
        setFeaturedNews({
          title: latestArticle.title,
          shortdesc: latestArticle.shortdesc,
          fulldesc: latestArticle.fulldesc,
          picurl: latestArticle.picurl,
          date: latestArticle.date,
          author: latestArticle.author
        });

        // Set the rest as recent news
        const remainingArticles = sortedArticles.slice(1);
        setRecentNews(remainingArticles.map(article => ({
          title: article.title,
          shortdesc: article.shortdesc,
          fulldesc: article.fulldesc,
          picurl: article.picurl,
          date: article.date,
          author: article.author
        })));
      }
    }
    
    fetchNews();
  }, []);

  // Add handler for closing expanded article
  const handleClose = () => {
    setSelectedArticle(null);
    setIsExpanded(false);
  };
  return (
    <div className="homepage-container">
      {selectedArticle && (
        <>
          <div 
            className={`overlay ${isExpanded ? 'visible' : ''}`} 
            onClick={handleClose}
          />
          <div className={`expanded-article ${isExpanded ? 'visible' : ''}`}>
            <button className="close-button" onClick={handleClose}>×</button>
            <img 
              src={selectedArticle.picurl ? `${newsApi.defaults.baseURL}/images/${selectedArticle.picurl}` : "/placeholder.svg"}  
              alt={selectedArticle.title} 
              className="expanded-image" 
            />
            <div className="expanded-content">
              <h2>{selectedArticle.title}</h2>
              <span className="news-date">{selectedArticle.date}</span>
              <p className="news-description">{selectedArticle.fulldesc}</p>
            </div>
          </div>
        </>
      )}
      
      <header className="homepage-header">
        <h1>NewsHub</h1>
        <p>Your trusted source for daily news</p>
      </header>

      <main>
        <section 
          className="featured-news"
          onClick={() => {
            setSelectedArticle(featuredNews);
            setIsExpanded(true);
          }}
          style={{ cursor: 'pointer' }}
        >
          <img 
            src={featuredNews.picurl ? `${newsApi.defaults.baseURL}/images/${featuredNews.picurl}` : "/placeholder.svg"} 
            alt={featuredNews.title} 
            className="featured-image" 
          />
          <div className="featured-content">
            <h2>{featuredNews.title}</h2>
            <span className="news-date">{featuredNews.date}</span>
            <p className="news-description">{featuredNews.shortdesc}</p>
          </div>
        </section>
        
        <section>
          <h2 className="section-title">Recent News</h2>
          <div className="recent-news-grid">
            {recentNews.map((article, index) => (
              <article 
                key={index} 
                className="news-card"
                onClick={() => {
                  setSelectedArticle(article);
                  setIsExpanded(true);
                }}
                style={{ cursor: 'pointer' }}
              >
                <img 
                  src={article.picurl ? `${newsApi.defaults.baseURL}/images/${article.picurl}` : "/placeholder.svg"} 
                  alt={article.title} 
                  className="card-image" 
                />
                <div className="card-content">
                  <h3 className="news-title">{article.title}</h3>
                  <span className="news-date">{article.date}</span>
                  <p className="news-description">{article.shortdesc}</p>
                </div>
              </article>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default HomePage;

