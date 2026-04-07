#!/usr/bin/env python3
"""
Vector Database Management for Banking Assistant System
Creates and manages FAISS index for fast similarity search
"""

import os
import sys
import json
import logging
import numpy as np
import pandas as pd
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pickle

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VectorDatabase:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.embedding_model = None
        self.index = None
        self.processed_data = None
        self.vector_db_path = Path(self.config['vector_database']['path'])
        self.vector_db_path.mkdir(exist_ok=True)
        
    def load_config(self, config_path):
        """Load configuration file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            logger.info("Please run setup_models.py first")
            sys.exit(1)
    
    def load_embedding_model(self):
        """Load the embedding model"""
        try:
            logger.info("Loading embedding model...")
            model_name = self.config['models']['embedding_model']
            self.embedding_model = SentenceTransformer(model_name)
            logger.info(f"✅ Embedding model loaded: {model_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            return False
    
    def load_processed_data(self):
        """Load processed banking dataset"""
        try:
            data_path = self.config['preprocessing']['processed_data_path']
            logger.info(f"Loading processed data from {data_path}...")
            
            self.processed_data = pd.read_csv(data_path)
            logger.info(f"✅ Loaded {len(self.processed_data)} records")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load processed data: {e}")
            return False
    
    def create_embeddings(self, texts, batch_size=32):
        """Create embeddings for texts"""
        logger.info("Creating embeddings...")
        embeddings = []
        
        for i in tqdm(range(0, len(texts), batch_size), desc="Creating embeddings"):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings)
    
    def build_index(self):
        """Build FAISS index"""
        try:
            logger.info("Building FAISS index...")
            
            # Get texts for embedding
            texts = self.processed_data['embedding_text'].tolist()
            
            # Create embeddings
            embeddings = self.create_embeddings(texts)
            
            # Get embedding dimension
            dimension = embeddings.shape[1]
            logger.info(f"Embedding dimension: {dimension}")
            
            # Create FAISS index
            index_type = self.config['vector_database']['index_type']
            if index_type == 'IndexFlatIP':
                self.index = faiss.IndexFlatIP(dimension)
            elif index_type == 'IndexFlatL2':
                self.index = faiss.IndexFlatL2(dimension)
            else:
                logger.warning(f"Unknown index type: {index_type}, using IndexFlatIP")
                self.index = faiss.IndexFlatIP(dimension)
            
            # Add embeddings to index
            self.index.add(embeddings.astype('float32'))
            
            logger.info(f"✅ Index built with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to build index: {e}")
            return False
    
    def save_index(self):
        """Save FAISS index and metadata"""
        try:
            # Save index
            index_path = self.vector_db_path / 'faiss_index.bin'
            faiss.write_index(self.index, str(index_path))
            
            # Save metadata
            metadata = {
                'total_vectors': self.index.ntotal,
                'dimension': self.index.d,
                'index_type': self.config['vector_database']['index_type'],
                'model_name': self.config['models']['embedding_model']
            }
            
            metadata_path = self.vector_db_path / 'metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # Save processed data mapping
            data_mapping = {
                'indices': list(range(len(self.processed_data))),
                'categories': self.processed_data['category'].tolist(),
                'intents': self.processed_data['intent'].tolist()
            }
            
            mapping_path = self.vector_db_path / 'data_mapping.pkl'
            with open(mapping_path, 'wb') as f:
                pickle.dump(data_mapping, f)
            
            logger.info("✅ Index and metadata saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to save index: {e}")
            return False
    
    def load_index(self):
        """Load existing FAISS index"""
        try:
            index_path = self.vector_db_path / 'faiss_index.bin'
            metadata_path = self.vector_db_path / 'metadata.json'
            
            if not index_path.exists() or not metadata_path.exists():
                logger.warning("Index not found, building new one...")
                return False
            
            # Load index
            self.index = faiss.read_index(str(index_path))
            
            # Load metadata
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            logger.info(f"✅ Index loaded: {metadata['total_vectors']} vectors, {metadata['dimension']} dimensions")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load index: {e}")
            return False
    
    def search_similar(self, query, top_k=5):
        """Search for similar texts"""
        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query])
            
            # Search index
            scores, indices = self.index.search(query_embedding, top_k)
            
            # Get results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.processed_data):
                    result = {
                        'rank': i + 1,
                        'score': float(score),
                        'category': self.processed_data.iloc[idx]['category'],
                        'intent': self.processed_data.iloc[idx]['intent'],
                        'instruction': self.processed_data.iloc[idx]['instruction_clean'],
                        'response': self.processed_data.iloc[idx]['response_structured'],
                        'rag_content': self.processed_data.iloc[idx]['rag_content']
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []
    
    def test_search(self):
        """Test search functionality"""
        test_queries = [
            "How do I activate my credit card?",
            "I need to find an ATM near me",
            "How do I apply for a loan?",
            "What are the fees for international transfers?",
            "I lost my card, what should I do?"
        ]
        
        logger.info("Testing search functionality...")
        
        for query in test_queries:
            logger.info(f"\nQuery: {query}")
            results = self.search_similar(query, top_k=3)
            
            for result in results:
                logger.info(f"  Rank {result['rank']}: {result['category']} - {result['intent']} (Score: {result['score']:.3f})")
    
    def get_statistics(self):
        """Get database statistics"""
        if self.index is None:
            logger.error("Index not loaded")
            return None
        
        stats = {
            'total_vectors': self.index.ntotal,
            'dimension': self.index.d,
            'index_type': type(self.index).__name__,
            'categories': self.processed_data['category'].value_counts().to_dict(),
            'intents': self.processed_data['intent'].value_counts().head(10).to_dict()
        }
        
        return stats
    
    def rebuild_index(self):
        """Rebuild the entire index"""
        logger.info("Rebuilding vector database...")
        
        # Remove existing files
        for file in self.vector_db_path.glob('*'):
            file.unlink()
        
        # Build new index
        return self.build_index() and self.save_index()

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Vector Database Management')
    parser.add_argument('--rebuild', action='store_true', help='Rebuild the entire index')
    parser.add_argument('--test', action='store_true', help='Test search functionality')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    # Initialize vector database
    vdb = VectorDatabase()
    
    if args.rebuild:
        # Rebuild index
        if vdb.load_embedding_model() and vdb.load_processed_data():
            if vdb.rebuild_index():
                logger.info("✅ Vector database rebuilt successfully")
            else:
                logger.error("❌ Failed to rebuild vector database")
                sys.exit(1)
    else:
        # Load existing index or build new one
        if not vdb.load_index():
            if vdb.load_embedding_model() and vdb.load_processed_data():
                if vdb.build_index() and vdb.save_index():
                    logger.info("✅ Vector database created successfully")
                else:
                    logger.error("❌ Failed to create vector database")
                    sys.exit(1)
            else:
                logger.error("❌ Failed to load models or data")
                sys.exit(1)
    
    if args.test:
        vdb.test_search()
    
    if args.stats:
        stats = vdb.get_statistics()
        if stats:
            logger.info("Database Statistics:")
            logger.info(f"  Total vectors: {stats['total_vectors']}")
            logger.info(f"  Dimension: {stats['dimension']}")
            logger.info(f"  Index type: {stats['index_type']}")
            logger.info(f"  Categories: {len(stats['categories'])}")
            logger.info(f"  Intents: {len(stats['intents'])}")

if __name__ == "__main__":
    main()
