#!/usr/bin/env python3
"""
Main Banking Assistant System
Integrates Hugging Face MiniLM V62 with RAG pipeline for intelligent banking support
"""

import os
import sys
import json
import logging
import time
import re
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel, pipeline
import torch

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankingAssistant:
    def __init__(self, config_path='config.json'):
        self.config = self.load_config(config_path)
        self.embedding_model = None
        self.generation_model = None
        self.tokenizer = None
        self.vector_db = None
        self.processed_data = None
        self.pii_patterns = self.load_pii_patterns()
        
        # Initialize components
        self.initialize_models()
        self.load_data()
        
    def load_config(self, config_path):
        """Load configuration file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            logger.info("Please run setup_models.py first")
            sys.exit(1)
    
    def load_pii_patterns(self):
        """Load PII detection patterns"""
        return {
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
    
    def initialize_models(self):
        """Initialize Hugging Face models"""
        try:
            logger.info("Initializing models...")
            
            # Load embedding model (MiniLM V62)
            embedding_model_name = self.config['models']['embedding_model']
            self.embedding_model = SentenceTransformer(embedding_model_name)
            logger.info(f"✅ Embedding model loaded: {embedding_model_name}")
            
            # Load generation model
            generation_model_name = self.config['models']['generation_model']
            self.tokenizer = AutoTokenizer.from_pretrained(generation_model_name)
            self.generation_model = AutoModel.from_pretrained(generation_model_name)
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"✅ Generation model loaded: {generation_model_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize models: {e}")
            sys.exit(1)
    
    def load_data(self):
        """Load processed data and vector database"""
        try:
            # Load processed data
            data_path = self.config['preprocessing']['processed_data_path']
            self.processed_data = pd.read_csv(data_path)
            logger.info(f"✅ Loaded {len(self.processed_data)} records")
            
            # Load vector database
            from vector_database import VectorDatabase
            self.vector_db = VectorDatabase()
            if not self.vector_db.load_index():
                logger.warning("Vector database not found, building...")
                if self.vector_db.load_embedding_model() and self.vector_db.load_processed_data():
                    if self.vector_db.build_index() and self.vector_db.save_index():
                        logger.info("✅ Vector database built successfully")
                    else:
                        logger.error("❌ Failed to build vector database")
                        sys.exit(1)
                else:
                    logger.error("❌ Failed to load models or data for vector database")
                    sys.exit(1)
            else:
                logger.info("✅ Vector database loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to load data: {e}")
            sys.exit(1)
    
    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect PII in text"""
        pii_found = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                pii_found[pii_type] = matches
        
        return pii_found
    
    def mask_pii(self, text: str) -> str:
        """Mask PII in text"""
        masked_text = text
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if pii_type == 'credit_card':
                    masked = '*' * (len(match) - 4) + match[-4:]
                elif pii_type == 'ssn':
                    masked = '***-**-' + match[-4:]
                elif pii_type == 'phone':
                    masked = '***-***-' + match[-4:]
                elif pii_type == 'email':
                    parts = match.split('@')
                    masked = parts[0][:2] + '*' * (len(parts[0]) - 2) + '@' + parts[1]
                
                masked_text = masked_text.replace(match, masked)
        
        return masked_text
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant context using vector search"""
        try:
            # Search vector database
            results = self.vector_db.search_similar(query, top_k)
            
            # Filter results by relevance score
            relevant_results = [r for r in results if r['score'] > 0.3]
            
            if not relevant_results:
                logger.warning("No relevant context found, using fallback")
                # Return some general banking responses
                fallback_results = self.processed_data[
                    self.processed_data['category'].isin(['CONTACT', 'CUSTOMER_SERVICE'])
                ].head(top_k)
                
                relevant_results = []
                for _, row in fallback_results.iterrows():
                    relevant_results.append({
                        'category': row['category'],
                        'intent': row['intent'],
                        'response': row['response_structured'],
                        'score': 0.1
                    })
            
            return relevant_results
            
        except Exception as e:
            logger.error(f"❌ Context retrieval failed: {e}")
            return []
    
    def generate_response(self, query: str, contexts: List[Dict]) -> str:
        """Generate response using retrieved context"""
        try:
            if not contexts:
                return "I apologize, but I couldn't find specific information for your query. Please contact our customer service for assistance."
            
            # Combine contexts
            context_text = "\n\n".join([
                f"Context {i+1} ({ctx['category']} - {ctx['intent']}): {ctx['response']}"
                for i, ctx in enumerate(contexts[:3])  # Use top 3 contexts
            ])
            
            # Create prompt
            prompt = f"""Based on the following banking context, provide a helpful and accurate response to the customer query.

Customer Query: {query}

Banking Context:
{context_text}

Response:"""
            
            # Generate response using the model
            inputs = self.tokenizer.encode(prompt, return_tensors='pt', max_length=512, truncation=True)
            
            with torch.no_grad():
                outputs = self.generation_model.generate(
                    inputs,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (after "Response:")
            if "Response:" in response:
                response = response.split("Response:")[-1].strip()
            
            # Clean up response
            response = response.replace('\n', ' ').strip()
            
            # If response is too short, use the best context
            if len(response) < 50 and contexts:
                response = contexts[0]['response']
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Response generation failed: {e}")
            # Fallback to best context
            if contexts:
                return contexts[0]['response']
            return "I apologize, but I'm having trouble generating a response. Please try again or contact customer service."
    
    def process_query(self, query: str, top_k: int = 5) -> Dict:
        """Process a customer query and return response"""
        start_time = time.time()
        
        try:
            # Check for PII
            pii_detected = self.detect_pii(query)
            if pii_detected:
                logger.warning(f"PII detected in query: {pii_detected}")
                query = self.mask_pii(query)
            
            # Retrieve relevant context
            contexts = self.retrieve_context(query, top_k)
            
            # Generate response
            response = self.generate_response(query, contexts)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Prepare result
            result = {
                'query': query,
                'response': response,
                'processing_time': processing_time,
                'contexts_used': len(contexts),
                'best_match': {
                    'category': contexts[0]['category'] if contexts else 'UNKNOWN',
                    'intent': contexts[0]['intent'] if contexts else 'UNKNOWN',
                    'confidence': contexts[0]['score'] if contexts else 0.0
                },
                'pii_detected': bool(pii_detected),
                'pii_types': list(pii_detected.keys()) if pii_detected else []
            }
            
            logger.info(f"Query processed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"❌ Query processing failed: {e}")
            return {
                'query': query,
                'response': "I apologize, but I encountered an error processing your request. Please try again or contact customer service.",
                'processing_time': time.time() - start_time,
                'error': str(e)
            }
    
    def get_statistics(self) -> Dict:
        """Get system statistics"""
        stats = {
            'total_records': len(self.processed_data),
            'categories': self.processed_data['category'].nunique(),
            'intents': self.processed_data['intent'].nunique(),
            'embedding_model': self.config['models']['embedding_model'],
            'generation_model': self.config['models']['generation_model']
        }
        
        if self.vector_db and self.vector_db.index:
            db_stats = self.vector_db.get_statistics()
            if db_stats:
                stats.update({
                    'vector_db_vectors': db_stats['total_vectors'],
                    'vector_db_dimension': db_stats['dimension']
                })
        
        return stats
    
    def test_system(self):
        """Test the system with sample queries"""
        test_queries = [
            "How do I activate my credit card?",
            "I need to find an ATM near me",
            "How do I apply for a loan?",
            "What are the fees for international transfers?",
            "I lost my card, what should I do?",
            "How do I check my account balance?",
            "Can I transfer money to another account?",
            "What are the requirements for opening a new account?"
        ]
        
        logger.info("Testing Banking Assistant System...")
        logger.info("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\nTest {i}: {query}")
            result = self.process_query(query)
            
            logger.info(f"Response: {result['response'][:100]}...")
            logger.info(f"Category: {result['best_match']['category']}")
            logger.info(f"Intent: {result['best_match']['intent']}")
            logger.info(f"Confidence: {result['best_match']['confidence']:.3f}")
            logger.info(f"Processing time: {result['processing_time']:.2f}s")
            
            if result['pii_detected']:
                logger.warning(f"PII detected: {result['pii_types']}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Banking Assistant System')
    parser.add_argument('--test', action='store_true', help='Test the system')
    parser.add_argument('--stats', action='store_true', help='Show system statistics')
    parser.add_argument('--query', type=str, help='Process a specific query')
    
    args = parser.parse_args()
    
    # Initialize banking assistant
    assistant = BankingAssistant()
    
    if args.stats:
        stats = assistant.get_statistics()
        logger.info("System Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
    
    elif args.test:
        assistant.test_system()
    
    elif args.query:
        result = assistant.process_query(args.query)
        print(f"\nQuery: {result['query']}")
        print(f"Response: {result['response']}")
        print(f"Category: {result['best_match']['category']}")
        print(f"Intent: {result['best_match']['intent']}")
        print(f"Confidence: {result['best_match']['confidence']:.3f}")
        print(f"Processing time: {result['processing_time']:.2f}s")
    
    else:
        # Interactive mode
        print("🏦 Banking Assistant System")
        print("=" * 40)
        print("Type 'quit' to exit")
        print("Type 'stats' to see system statistics")
        print("Type 'test' to run system tests")
        print()
        
        while True:
            try:
                query = input("Customer: ").strip()
                
                if query.lower() == 'quit':
                    break
                elif query.lower() == 'stats':
                    stats = assistant.get_statistics()
                    print("\nSystem Statistics:")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                    print()
                elif query.lower() == 'test':
                    assistant.test_system()
                elif query:
                    result = assistant.process_query(query)
                    print(f"\nAssistant: {result['response']}")
                    print(f"[Category: {result['best_match']['category']}, Confidence: {result['best_match']['confidence']:.3f}]")
                    print()
                else:
                    print("Please enter a query.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()
