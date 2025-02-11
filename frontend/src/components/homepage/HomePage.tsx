import { useEffect, useState } from 'react';
import './HomePage.css';

// Mock data


const featuredNews = {
  title: "Breaking: Major Scientific Discovery Announced",
  description:
    "Scientists have made a groundbreaking discovery that could revolutionize our understanding of the universe.",
  image: "https://placehold.co/800x400",
  date: "2025-02-10",
}

const recentNews = [
  {
    title: "Tech Giant Unveils New AI-Powered Device",
    description: "The latest innovation promises to transform daily life with advanced artificial intelligence.",
    image: "https://placehold.co/300x200",
    date: "2025-02-09",
  },
  {
    title: "Global Climate Summit Reaches Landmark Agreement",
    description: "World leaders commit to ambitious targets in the fight against climate change.",
    image: "https://placehold.co/300x200",
    date: "2025-02-08",
  },
  {
    title: "Sports: Underdog Team Wins Championship in Stunning Upset",
    description: "In a David vs. Goliath story, the underdogs emerged victorious against all odds.",
    image: "https://placehold.co/300x200",
    date: "2025-02-07",
  },
  {
    title: "Sports: Underdog Team Wins Championship in Stunning Upset",
    description: "In a David vs. Goliath story, the underdogs emerged victorious against all odds.",
    image: "https://placehold.co/300x200",
    date: "2025-02-07",
  },
]

// Add this type definition
type NewsArticle = {
  title: string;
  description: string;
  image: string;
  date: string;
};

function HomePage() {
  // Add state for selected article
  const [selectedArticle, setSelectedArticle] = useState<NewsArticle | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    document.title = 'NewsHub - Your Daily News Source';
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
              src={selectedArticle.image || "/placeholder.svg"} 
              alt={selectedArticle.title} 
              className="expanded-image" 
            />
            <div className="expanded-content">
              <h2>{selectedArticle.title}</h2>
              <span className="news-date">{selectedArticle.date}</span>
              <p className="news-description">{selectedArticle.description}</p>
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
            src={featuredNews.image || "/placeholder.svg"} 
            alt={featuredNews.title} 
            className="featured-image" 
          />
          <div className="featured-content">
            <h2>{featuredNews.title}</h2>
            <span className="news-date">{featuredNews.date}</span>
            <p className="news-description">{featuredNews.description}</p>
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
                  src={article.image || "/placeholder.svg"} 
                  alt={article.title} 
                  className="card-image" 
                />
                <div className="card-content">
                  <h3 className="news-title">{article.title}</h3>
                  <span className="news-date">{article.date}</span>
                  <p className="news-description">{article.description}</p>
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

