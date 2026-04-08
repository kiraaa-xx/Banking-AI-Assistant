#!/usr/bin/env python3
"""
Setup script for Banking Assistant System
Downloads and configures required Hugging Face models
"""

import os
import sys
import logging
from pathlib import Path
import requests
from tqdm import tqdm
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelSetup:
    def __init__(self):
        self.models = {
            'embedding': 'sentence-transformers/all-MiniLM-L6-v2',
            'generation': 'microsoft/DialoGPT-medium',
            'tokenizer': 'microsoft/DialoGPT-medium'
        }
        self.model_dir = Path('./models')
        self.model_dir.mkdir(exist_ok=True)
        
    def check_api_key(self):
        """Check if Hugging Face API key is set"""
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            logger.error("HUGGINGFACE_API_KEY not found in environment variables")
            logger.info("Please set your API key: export HUGGINGFACE_API_KEY='your_key_here'")
            return False
        return True
    
    def download_model(self, model_name, model_path):
        """Download model from Hugging Face"""
        try:
            logger.info(f"Downloading {model_name}...")
            
            # Create model directory
            model_dir = self.model_dir / model_name
            model_dir.mkdir(exist_ok=True)
            
            # Download model files
            from huggingface_hub import snapshot_download
            
            snapshot_download(
                repo_id=model_path,
                local_dir=model_dir,
                local_dir_use_symlinks=False
            )
            
            logger.info(f"✅ {model_name} downloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to download {model_name}: {e}")
            return False
    
    def test_model_loading(self):
        """Test if models can be loaded correctly"""
        try:
            logger.info("Testing model loading...")
            
            # Test embedding model
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            
            # Test generation model
            from transformers import AutoTokenizer, AutoModel
            tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
            model = AutoModel.from_pretrained('microsoft/DialoGPT-medium')
            
            # Test with sample text
            test_text = "How do I activate my credit card?"
            embedding = embedding_model.encode([test_text])
            
            logger.info("✅ All models loaded successfully")
            logger.info(f"   Embedding dimension: {embedding.shape[1]}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model loading test failed: {e}")
            return False
    
    def create_config_file(self):
        """Create configuration file for the system"""
        config = {
            'models': {
                'embedding_model': 'sentence-transformers/all-MiniLM-L6-v2',
                'generation_model': 'microsoft/DialoGPT-medium',
                'embedding_dimension': 384
            },
            'vector_database': {
                'type': 'faiss',
                'index_type': 'IndexFlatIP',
                'path': './vector_database'
            },
            'preprocessing': {
                'processed_data_path': './processed_banking_dataset.csv',
                'max_text_length': 512
            },
            'api': {
                'batch_size': 32,
                'max_retries': 3,
                'timeout': 30
            }
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info("✅ Configuration file created: config.json")
    
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            './models',
            './vector_database',
            './logs',
            './data',
            './cache'
        ]
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
            logger.info(f"✅ Created directory: {directory}")
    
    def run_setup(self):
        """Run complete setup process"""
        logger.info("🚀 Starting Banking Assistant System Setup")
        logger.info("=" * 50)
        
        # Check API key
        if not self.check_api_key():
            return False
        
        # Create directories
        self.setup_directories()
        
        # Download models
        success_count = 0
        for model_name, model_path in self.models.items():
            if self.download_model(model_name, model_path):
                success_count += 1
        
        # Test model loading
        if self.test_model_loading():
            success_count += 1
        
        # Create config file
        self.create_config_file()
        
        logger.info("=" * 50)
        logger.info(f"Setup completed: {success_count}/{len(self.models) + 1} steps successful")
        
        if success_count == len(self.models) + 1:
            logger.info("🎉 All models downloaded and configured successfully!")
            logger.info("You can now run the banking assistant system.")
        else:
            logger.warning("⚠️ Some steps failed. Please check the logs above.")
        
        return success_count == len(self.models) + 1

def main():
    """Main setup function"""
    setup = ModelSetup()
    success = setup.run_setup()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("Next steps:")
        print("1. Run preprocessing: python preprocessing_pipeline.py")
        print("2. Create vector database: python vector_database.py")
        print("3. Start the system: python banking_assistant.py")
        print("4. Or use web interface: streamlit run web_interface.py")
    else:
        print("\n" + "=" * 50)
        print("❌ SETUP FAILED!")
        print("=" * 50)
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
