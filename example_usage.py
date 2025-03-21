#!/usr/bin/env python3
"""
Example usage of the API to CSV pipeline with JSONPlaceholder API.
"""

from api_to_csv import APIDataPipeline

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


# Example with GitHub API to fetch repository data
def fetch_github_repos(username="tensorflow"):
    # Initialize the pipeline with the GitHub API for a specific user's repos
    pipeline = APIDataPipeline(
        api_url=f"https://api.github.com/users/{username}/repos",
        output_dir="data/github"
    )
    
    # Run the pipeline
    output_path = pipeline.run_pipeline(filename=f"{username}_repos.csv")
    print(f"GitHub repositories for {username} saved to: {output_path}")


if __name__ == "__main__":
    # Run the examples
    fetch_posts()
    fetch_github_repos()