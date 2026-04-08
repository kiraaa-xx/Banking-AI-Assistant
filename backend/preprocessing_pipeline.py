import pandas as pd
import numpy as np
import re
import json
from typing import Dict, List, Tuple
import logging
from datetime import datetime
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BankingAssistantPreprocessor:
    def __init__(self):
        self.banking_terms = {
            'acivate': 'activate',
            'visa': 'Visa',
            'mastercard': 'Mastercard',
            'atm': 'ATM',
            'pin': 'PIN',
            'cvv': 'CVV',
            'cvc': 'CVC',
            'ssn': 'SSN',
            'routing': 'routing number',
            'account': 'account number'
        }
        
        self.banking_categories = {
            'CARD': 'card_services',
            'LOAN': 'loan_services', 
            'ACCOUNT': 'account_management',
            'TRANSFER': 'money_transfer',
            'ATM': 'atm_services',
            'PASSWORD': 'security_authentication',
            'FEES': 'fees_charges',
            'CONTACT': 'customer_support',
            'FIND': 'location_services'
        }
        
        # PII patterns for detection
        self.pii_patterns = {
            'credit_card': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load the dataset from CSV file"""
        logger.info(f"Loading dataset from {file_path}")
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if pd.isna(text):
            return ""
        
        # Convert to string
        text = str(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common banking typos
        for typo, correct in self.banking_terms.items():
            text = re.sub(rf'\b{typo}\b', correct, text, flags=re.IGNORECASE)
        
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\[\]\{\}]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        
        return text.strip()

    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        """Detect Personally Identifiable Information"""
        pii_found = {}
        
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                pii_found[pii_type] = matches
        
        return pii_found

    def mask_pii(self, text: str) -> Tuple[str, Dict[str, List[str]]]:
        """Mask PII in text and return masked text with detected PII"""
        pii_found = self.detect_pii(text)
        masked_text = text
        
        for pii_type, matches in pii_found.items():
            for match in matches:
                if pii_type == 'credit_card':
                    # Keep only last 4 digits
                    masked = '*' * (len(match) - 4) + match[-4:]
                elif pii_type == 'ssn':
                    # Keep only last 4 digits
                    masked = '***-**-' + match[-4:]
                elif pii_type == 'phone':
                    # Keep only last 4 digits
                    masked = '***-***-' + match[-4:]
                elif pii_type == 'email':
                    # Mask email domain
                    parts = match.split('@')
                    masked = parts[0][:2] + '*' * (len(parts[0]) - 2) + '@' + parts[1]
                
                masked_text = masked_text.replace(match, masked)
        
        return masked_text, pii_found

    def enhance_instruction(self, instruction: str, category: str) -> str:
        """Enhance instruction with banking context"""
        enhanced = instruction
        
        # Add banking context based on category
        if category == 'CARD':
            if 'activate' in instruction.lower():
                enhanced = f"[Card Activation Request] {instruction}"
            elif 'block' in instruction.lower():
                enhanced = f"[Card Security Request] {instruction}"
        elif category == 'LOAN':
            enhanced = f"[Loan Services] {instruction}"
        elif category == 'ACCOUNT':
            enhanced = f"[Account Management] {instruction}"
        elif category == 'TRANSFER':
            enhanced = f"[Money Transfer] {instruction}"
        
        return enhanced

    def structure_response(self, response: str, intent: str) -> str:
        """Structure response for better RAG retrieval"""
        # Add intent-based structure
        structured_response = response
        
        # Add response type metadata
        if 'step' in response.lower() or 'follow' in response.lower():
            structured_response = f"[STEP-BY-STEP GUIDE] {response}"
        elif 'contact' in response.lower() or 'call' in response.lower():
            structured_response = f"[CONTACT INFORMATION] {response}"
        elif 'security' in response.lower() or 'secure' in response.lower():
            structured_response = f"[SECURITY INFORMATION] {response}"
        
        return structured_response

    def create_metadata(self, row: pd.Series) -> Dict:
        """Create metadata for each entry"""
        return {
            'category': row['category'],
            'intent': row['intent'],
            'tags': row['tags'],
            'word_count': len(str(row['instruction']).split()),
            'response_length': len(str(row['response'])),
            'has_pii': bool(self.detect_pii(str(row['response']))),
            'processing_timestamp': datetime.now().isoformat()
        }

    def preprocess_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Main preprocessing pipeline"""
        logger.info("Starting preprocessing pipeline...")
        
        # Create a copy to avoid modifying original
        processed_df = df.copy()
        
        # Step 1: Clean text fields
        logger.info("Step 1: Cleaning text fields...")
        processed_df['instruction_clean'] = processed_df['instruction'].apply(self.clean_text)
        processed_df['response_clean'] = processed_df['response'].apply(self.clean_text)
        
        # Step 2: Detect and mask PII
        logger.info("Step 2: Detecting and masking PII...")
        pii_results = processed_df['response_clean'].apply(self.mask_pii)
        processed_df['response_masked'] = [result[0] for result in pii_results]
        processed_df['pii_detected'] = [result[1] for result in pii_results]
        
        # Step 3: Enhance instructions
        logger.info("Step 3: Enhancing instructions...")
        processed_df['instruction_enhanced'] = processed_df.apply(
            lambda row: self.enhance_instruction(row['instruction_clean'], row['category']), axis=1
        )
        
        # Step 4: Structure responses
        logger.info("Step 4: Structuring responses...")
        processed_df['response_structured'] = processed_df.apply(
            lambda row: self.structure_response(row['response_masked'], row['intent']), axis=1
        )
        
        # Step 5: Create metadata
        logger.info("Step 5: Creating metadata...")
        processed_df['metadata'] = processed_df.apply(self.create_metadata, axis=1)
        
        # Step 6: Create RAG-ready fields
        logger.info("Step 6: Creating RAG-ready fields...")
        processed_df['rag_content'] = processed_df.apply(
            lambda row: f"Question: {row['instruction_enhanced']}\nAnswer: {row['response_structured']}", axis=1
        )
        
        # Step 7: Add embeddings-ready text
        processed_df['embedding_text'] = processed_df['rag_content'].apply(self.clean_text)
        
        logger.info("Preprocessing completed successfully!")
        return processed_df

    def validate_preprocessing(self, df: pd.DataFrame) -> Dict:
        """Validate preprocessing results"""
        validation_results = {
            'total_records': len(df),
            'records_with_pii': len(df[df['pii_detected'].apply(bool)]),
            'categories_processed': df['category'].nunique(),
            'intents_processed': df['intent'].nunique(),
            'avg_response_length': df['response_clean'].str.len().mean(),
            'avg_instruction_length': df['instruction_clean'].str.len().mean()
        }
        
        logger.info("Validation Results:")
        for key, value in validation_results.items():
            logger.info(f"  {key}: {value}")
        
        return validation_results

    def save_processed_data(self, df: pd.DataFrame, output_path: str):
        """Save processed dataset"""
        logger.info(f"Saving processed data to {output_path}")
        
        # Save main processed dataset
        df.to_csv(output_path, index=False)
        
        # Save metadata summary
        metadata_summary = {
            'processing_info': {
                'timestamp': datetime.now().isoformat(),
                'total_records': len(df),
                'categories': df['category'].value_counts().to_dict(),
                'intents': df['intent'].value_counts().head(20).to_dict()
            },
            'pii_summary': {
                'records_with_pii': len(df[df['pii_detected'].apply(bool)]),
                'pii_types_found': self._get_pii_summary(df)
            }
        }
        
        with open(output_path.replace('.csv', '_metadata.json'), 'w') as f:
            json.dump(metadata_summary, f, indent=2)
        
        logger.info("Data saved successfully!")

    def _get_pii_summary(self, df: pd.DataFrame) -> Dict:
        """Get summary of PII types found"""
        pii_summary = {}
        for pii_data in df['pii_detected']:
            for pii_type in pii_data.keys():
                pii_summary[pii_type] = pii_summary.get(pii_type, 0) + 1
        return pii_summary

def main():
    """Main execution function"""
    # Initialize preprocessor
    preprocessor = BankingAssistantPreprocessor()
    
    # Load data
    df = preprocessor.load_data('dataset.csv')
    
    # Preprocess data
    processed_df = preprocessor.preprocess_dataset(df)
    
    # Validate results
    validation_results = preprocessor.validate_preprocessing(processed_df)
    
    # Save processed data
    preprocessor.save_processed_data(processed_df, 'processed_banking_dataset.csv')
    
    # Print summary
    print("\n" + "="*50)
    print("PREPROCESSING COMPLETED SUCCESSFULLY!")
    print("="*50)
    print(f"Original records: {len(df)}")
    print(f"Processed records: {len(processed_df)}")
    print(f"Records with PII detected: {validation_results['records_with_pii']}")
    print(f"Categories processed: {validation_results['categories_processed']}")
    print(f"Intents processed: {validation_results['intents_processed']}")
    print("\nFiles created:")
    print("- processed_banking_dataset.csv (main dataset)")
    print("- processed_banking_dataset_metadata.json (metadata summary)")

if __name__ == "__main__":
    main()
