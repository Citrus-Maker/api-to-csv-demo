#!/usr/bin/env python3
"""
Example usage of the API to CSV pipeline with JSONPlaceholder API.
"""

from api_to_csv import APIDataPipeline
import requests
import pandas as pd
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Example with JSONPlaceholder API (free, public API for testing)
def fetch_posts():
    # Initialize the pipeline with the JSONPlaceholder posts API
    pipeline = APIDataPipeline(
        api_url="https://jsonplaceholder.typicode.com/posts",
        output_dir="data/posts"
    )
    
    # Run the pipeline
    output_path = pipeline.run_pipeline(filename="posts_data.csv")
    print(f"Posts data saved to: {output_path}")


# Custom GitHub repos example that handles nested JSON data
def fetch_github_repos(username="tensorflow"):
    output_dir = "data/github"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    logger.info(f"Fetching GitHub repositories for user: {username}")
    api_url = f"https://api.github.com/users/{username}/repos"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        repos_data = response.json()
        logger.info(f"Successfully fetched {len(repos_data)} repositories")
        
        # Extract only the fields we want (flattening the nested structure)
        simplified_data = []
        for repo in repos_data:
            simplified_data.append({
                'id': repo.get('id'),
                'name': repo.get('name'),
                'full_name': repo.get('full_name'),
                'description': repo.get('description'),
                'html_url': repo.get('html_url'),
                'language': repo.get('language'),
                'stargazers_count': repo.get('stargazers_count'),
                'forks_count': repo.get('forks_count'),
                'created_at': repo.get('created_at'),
                'updated_at': repo.get('updated_at'),
                'size': repo.get('size'),
                'default_branch': repo.get('default_branch'),
                'open_issues_count': repo.get('open_issues_count'),
                'topics': ','.join(repo.get('topics', [])) if repo.get('topics') else '',
                'is_fork': repo.get('fork', False)
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(simplified_data)
        
        # Add extraction timestamp
        df['extraction_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save to CSV
        filename = f"{username}_repos.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        
        logger.info(f"GitHub repositories saved to: {filepath}")
        return filepath
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching GitHub repositories: {e}")
        raise


if __name__ == "__main__":
    # Run the examples
    fetch_posts()
    fetch_github_repos()