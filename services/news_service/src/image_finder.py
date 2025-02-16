from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from pathlib import Path

def find_similar_image(text_query: str) -> tuple[str, float]:
    """
    Find most similar image for given text query.
    Returns tuple of (image_filename, similarity_score)
    """
    # Load environment variables
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)

    # Initialize CLIP and Pinecone
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    index = pc.Index("images4articles-kaban")

    # Process the text query
    inputs = processor(text=text_query, return_tensors="pt", padding=True)
    text_features = model.get_text_features(**inputs)
    text_vector = text_features.detach().numpy()[0].tolist()

    # Query Pinecone
    results = index.query(
        vector=text_vector,
        top_k=1,
        include_metadata=True
    )

    if results.matches:
        return results.matches[0].metadata['filename'], results.matches[0].score
    return None, 0.0 