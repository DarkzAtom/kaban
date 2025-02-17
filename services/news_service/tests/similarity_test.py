from transformers import CLIPProcessor, CLIPModel
from pinecone import Pinecone
import os
from dotenv import load_dotenv
from pathlib import Path

def test_image_search():
    # Load environment variables
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)

    # Initialize CLIP and Pinecone
    model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
    index = pc.Index("images4articles-kaban")  # or whatever your index name is

    # Test query text ls
    test_text = "headphones"  # you can change this to any description

    # Process the text query
    inputs = processor(text=test_text, return_tensors="pt", padding=True)
    text_features = model.get_text_features(**inputs)
    text_vector = text_features.detach().numpy()[0].tolist()

    # Query Pinecone
    results = index.query(
        vector=text_vector,
        top_k=3,  # get top 3 most similar images
        include_metadata=True
    )

    # Print results
    print(f"\nSearch results for: '{test_text}'")
    print("-------------------")
    for match in results.matches:
        print(f"Score: {match.score:.3f}")
        print(f"Image path: {match.metadata['path']}")
        print("-------------------")

if __name__ == "__main__":
    test_image_search()