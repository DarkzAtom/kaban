from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from pinecone import Pinecone, ServerlessSpec
import torch
from pathlib import Path
from tqdm import tqdm
import logging
import os
from dotenv import load_dotenv

# Get the path to the .env file (one directory up)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)



class ImageIndexer:
    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Initialize CLIP with larger model
        self.logger.info("Loading CLIP model...")
        self.model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
        
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        
        # Initialize Pinecone (V2)
        self.logger.info("Connecting to Pinecone...")
        self.pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
        
        # Create or get index
        index_name = "images4articles-kaban"
        if index_name not in self.pc.list_indexes().names():
            self.logger.info(f"Creating new index: {index_name}")
            self.pc.create_index(
                name=index_name,
                dimension=768,  # Changed from 512 to 768 for large model
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        
        self.index = self.pc.Index(index_name)

    def process_image(self, image_path):
        """Process a single image to vector"""
        try:
            # Open and convert image to RGB (handles PNG, JPEG, etc.)
            image = Image.open(image_path).convert('RGB')
            
            # Process through CLIP
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            with torch.no_grad():  # No need to track gradients
                image_features = self.model.get_image_features(**inputs)
            
            # Move to CPU and convert to list
            return image_features.cpu().numpy()[0].tolist()
            
        except Exception as e:
            self.logger.error(f"Error processing {image_path}: {str(e)}")
            return None

    def index_images(self, image_folder, batch_size=100):
        """Index all images from a folder"""
        # Get all image files
        image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
        image_paths = [
            p for p in Path(image_folder).rglob("*")
            if p.suffix.lower() in image_extensions
        ]
        
        if not image_paths:
            self.logger.warning(f"No images found in {image_folder}")
            return
        
        self.logger.info(f"Found {len(image_paths)} images to process")
        
        # Process images in batches
        vectors_batch = []
        
        for img_path in tqdm(image_paths, desc="Processing images"):
            vector = self.process_image(img_path)
            
            if vector:  # if processing was successful
                vectors_batch.append({
                    "id": img_path.name,
                    "values": vector,
                    "metadata": {
                        "path": str(img_path),
                        "filename": img_path.name
                    }
                })
            
            # When batch is full or on last item, upload to Pinecone
            if len(vectors_batch) >= batch_size or img_path == image_paths[-1]:
                if vectors_batch:  # if there's anything to upload
                    try:
                        self.index.upsert(vectors=vectors_batch)
                        self.logger.info(f"Uploaded batch of {len(vectors_batch)} vectors")
                        vectors_batch = []  # Clear batch after upload
                    except Exception as e:
                        self.logger.error(f"Error uploading batch: {str(e)}")

if __name__ == "__main__":
    # Set your environment variables
    
    indexer = ImageIndexer()
    
    # Get the path to the images folder
    image_folder = Path(__file__).parent.parent / "images" / "430_colored_images_test"

    
    indexer.index_images(image_folder)