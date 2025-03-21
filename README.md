# API to CSV Data Pipeline

A flexible data engineering tool that extracts data from APIs and transforms it into CSV format. This project demonstrates ETL (Extract, Transform, Load) principles and can be used with any REST API that returns JSON data.

## Features

- **Modular ETL Pipeline**: Follows best practices for data extraction, transformation, and loading
- **Flexible API Integration**: Works with any REST API endpoint
- **Data Transformation**: Handles deduplication, missing values, and adds metadata
- **Configurable Output**: Customizable output directory and file naming
- **Robust Logging**: Comprehensive logging for tracking pipeline execution
- **Command Line Interface**: Easy to use from the command line with various options

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/api-to-csv-pipeline.git
cd api-to-csv-pipeline
```

2. Install dependencies:
```
pip install requests pandas
```

## Usage

### Command Line Interface

Run the script with command line arguments:

```
python api_to_csv.py --api-url https://jsonplaceholder.typicode.com/posts --output-dir data --output-file my_data.csv
```

### Python Module

Import and use in your own Python code:

```python
from api_to_csv import APIDataPipeline

# Initialize the pipeline
pipeline = APIDataPipeline(
    api_url="https://jsonplaceholder.typicode.com/posts",
    output_dir="data/posts"
)

# Run the pipeline
output_path = pipeline.run_pipeline(filename="posts_data.csv")
print(f"Data saved to: {output_path}")
```

## Example Implementations

Check out `example_usage.py` for sample implementations with:
- JSONPlaceholder API (blog posts data)
- GitHub API (repository data)

To run the examples:
```
python example_usage.py
```

## Customization

The transformation logic in the `transform()` method can be customized based on your specific data needs:

```python
def transform(self, data):
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add your custom transformations here
    # ...
    
    return df
```

## Project Structure

```
.
├── api_to_csv.py           # Main pipeline module
├── example_usage.py        # Example implementation
├── data/                   # Output directory for CSV files
│   ├── posts/              # JSONPlaceholder posts data
│   └── github/             # GitHub repos data
└── README.md               # This documentation file
```

## Requirements

- Python 3.6+
- requests
- pandas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.