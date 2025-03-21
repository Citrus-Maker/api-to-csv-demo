#!/usr/bin/env python3
"""
API to CSV Data Pipeline

This script fetches data from a public API, transforms it, and saves it to a CSV file.
It demonstrates basic data engineering skills including API interaction, data transformation,
and file output operations.
"""

import requests
import pandas as pd
import json
import logging
import os
from datetime import datetime
import argparse
from typing import Dict, List, Any, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIDataPipeline:
    """A simple data pipeline to extract data from an API and transform it to CSV."""
    
    def __init__(self, api_url: str, output_dir: str = "data"):
        """
        Initialize the data pipeline.
        
        Args:
            api_url: The URL of the API to fetch data from
            output_dir: Directory to save output CSV files
        """
        self.api_url = api_url
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
    
    def extract(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Extract data from the API.
        
        Args:
            params: Optional parameters to pass to the API
            
        Returns:
            List of dictionaries containing the API response data
        """
        logger.info(f"Fetching data from {self.api_url}")
        
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} records from API")
            return data
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from API: {e}")
            raise
    
    def transform(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Transform the API data into a pandas DataFrame.
        
        Args:
            data: List of dictionaries containing the API response data
            
        Returns:
            Pandas DataFrame with transformed data
        """
        logger.info("Transforming data")
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Example transformations (customize based on your specific API data)
        # 1. Remove any duplicate records
        df_deduplicated = df.drop_duplicates()
        if len(df) - len(df_deduplicated) > 0:
            logger.info(f"Removed {len(df) - len(df_deduplicated)} duplicate records")
        
        # 2. Handle any missing values
        df_clean = df_deduplicated.fillna("N/A")
        
        # 3. Add a timestamp column to track when the data was collected
        df_clean['extraction_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Transformed data shape: {df_clean.shape}")
        return df_clean
    
    def load(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """
        Load the transformed data into a CSV file.
        
        Args:
            df: Pandas DataFrame with the transformed data
            filename: Optional filename for the CSV file
            
        Returns:
            Path to the saved CSV file
        """
        if filename is None:
            filename = f"data_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"Saving data to {filepath}")
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        logger.info(f"Successfully saved {len(df)} records to CSV")
        
        return filepath
    
    def run_pipeline(self, params: Optional[Dict[str, Any]] = None, filename: Optional[str] = None) -> str:
        """
        Run the complete ETL pipeline.
        
        Args:
            params: Optional parameters to pass to the API
            filename: Optional filename for the output CSV
            
        Returns:
            Path to the saved CSV file
        """
        logger.info("Starting pipeline run")
        
        # Extract
        raw_data = self.extract(params)
        
        # Transform
        transformed_data = self.transform(raw_data)
        
        # Load
        output_path = self.load(transformed_data, filename)
        
        logger.info("Pipeline run completed successfully")
        return output_path


def main():
    """Main function to run the pipeline with command line arguments."""
    parser = argparse.ArgumentParser(description="Fetch data from an API and save to CSV")
    parser.add_argument("--api-url", required=True, help="URL of the API to fetch data from")
    parser.add_argument("--output-dir", default="data", help="Directory to save the CSV file")
    parser.add_argument("--output-file", help="Name of the output CSV file")
    args = parser.parse_args()
    
    try:
        pipeline = APIDataPipeline(api_url=args.api_url, output_dir=args.output_dir)
        output_path = pipeline.run_pipeline(filename=args.output_file)
        print(f"Data successfully saved to: {output_path}")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        return 1
    
    return 0


# Example usage
if __name__ == "__main__":
    # For quick testing without command line args, uncomment and modify these lines:
    # api_url = "https://jsonplaceholder.typicode.com/posts"  # Example public API
    # pipeline = APIDataPipeline(api_url=api_url)
    # pipeline.run_pipeline()
    
    # Run with command line arguments
    exit(main())