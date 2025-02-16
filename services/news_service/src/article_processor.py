from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

class ArticleProcessor:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # OpenAI's GPT-4o-mini model
            temperature=0.3,
            api_key=os.getenv('OPENAI_API_KEY')
        )

        self.prompt = ChatPromptTemplate.from_template(
            """You are an expert at describing images. Given an article, you provide a short, 
            clear description of what kind of image would best represent this article.
            
            Rules:
            1. Keep the description under 1-4 words
            2. Focus on the main subject/theme
            3. Be specific but concise
            4. Don't use articles (a, an, the) unless absolutely necessary
            
            Article Title: {title}
            Article Content: {content}
            
            Provide only the image description, nothing else."""
        )

    def get_image_description(self, title: str, content: str) -> str:
        """Generate a concise image description from article content"""
        messages = self.prompt.format_messages(
            title=title,
            content=content
        )
        
        response = self.llm.invoke(messages)
        return response.content.strip()


# Example usage
if __name__ == "__main__":
    processor = ArticleProcessor()
    
    # Test with a sample article
    test_title = "World Leaders Gather for Davos Economic Forum"
    test_content = """The World Economic Forum's annual meeting in Davos, Switzerland, 
    kicked off today with global leaders discussing pressing economic challenges. 
    CEOs and heads of state gathered to address issues ranging from artificial intelligence 
    to climate change..."""
    
    description = processor.get_image_description(test_title, test_content)
    print(f"Generated image description: {description}")