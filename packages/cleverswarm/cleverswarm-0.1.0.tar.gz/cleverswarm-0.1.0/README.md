# CleverSwarm Python Client Library

A Python client library for interacting with CleverSwarm's REST API.

## Features

- Easy-to-use Python client for CleverSwarm API
- Create and manage text-to-knowledge graph extraction jobs
- Benchmark and evaluate knowledge graph extraction performance
- CLI application for text-to-KG conversion

## Prerequisites

- Python 3.7+
- CleverSwarm REST API endpoints running locally or on a server
- Access credentials for the CleverSwarm API

## Installation

```bash
pip install cleverswarm
```

For development:

```bash
pip install cleverswarm[dev]
```

## Dependencies

### External Dependencies

- **CleverSwarm REST API**: You must have the CleverSwarm REST API endpoints running. This is provided by the `rest_main` server.
- **Python Packages**:
  - `requests`: For HTTP communication
  - `tqdm`: For progress bars
  - `pydantic`: For data validation
  - `click`: For CLI functionality
  - `rich`: For enhanced terminal output

### Internal Dependencies

The client library consists of several modules:
- `client`: Core API client functionality
- `models`: Data models for API interactions
- `cli`: Command-line interface tools
- `utils`: Utility functions

## Setting up the Server

Before using the client, you must have the CleverSwarm REST API endpoints running:

1. Ensure you have the CleverSwarm server code
2. Start the REST API server:

```bash
# Navigate to the server directory
cd path_to_cleverswarm_endpoints

# Start the REST API server
python rest_main.py
```

The server typically runs on http://localhost:8000/ by default.

## Basic Usage

### Client Library

```python
from cleverswarm.client import CleverSwarmClient
from cleverswarm.client import JobStatus, FileTypeAPI

# Create a client instance
client = CleverSwarmClient(
    base_url="http://localhost:8000/",  # Point to your running REST API server
    username="your_username",  # Optional: Can be provided later via prompt
    token="your_token"  # Optional: Can be generated via client.update_token()
)

# If you don't have a token, you can log in 
client.update_token()  # This will prompt for username/password

# Get a list of jobs
jobs = client.get_jobs_list(is_benchmark=False)
print(f"Found {len(jobs)} text-to-KG jobs")

# Create a text-to-KG job
from pathlib import Path
job_id = client.create_unstructured_to_kg_job(
    unstructured_text_file=Path("input.txt"),
    ontology_file=Path("ontology.json"),
    ontology_spec_file=Path("ontology.owl"),
    force_filetype=FileTypeAPI.AutoDetect
)

# Wait for the job to complete
status = client.poll_job_ready_or_failed(job_id)

# Download the results
if status == JobStatus.Completed:
    client.retrieve_unstructured_to_kg_files(job_id, Path("output.json"))
```

### Text-to-KG CLI

The package provides a command-line interface for text-to-KG conversion. Before using it, ensure the CleverSwarm REST API server is running.

Basic usage:

```bash
text-to-kg --server_url http://localhost:8000/ \
           --input_prefix ./input \
           --output_prefix ./output \
           --mode run \
           --input_text document.txt \
           --ontology_json ontology.json \
           --ontology_owl ontology.owl
```

Full example with server job paths:

```bash
text-to-kg --server_url http://localhost:8000/ \
           --mode run \
           --input_prefix ./path_to_input_files \
           --output_prefix ./results \
           --input_text "Instituto Superior Tecnico.txt" \
           --ontology_json "1_university_ontology_with_descriptions.json" \
           --ontology_owl "ontology.owl" \
           --server_job_paths "path_to_cleverswarm_endpoints\jobs\outputs"
```

#### CLI Parameters Explained

- `--server_url`: URL of the running CleverSwarm REST API server
- `--mode`: Operation mode (`run`, `list`, `retry`, or `delete`)
- `--input_prefix`: Directory containing input files
- `--output_prefix`: Directory for saving output files
- `--input_text`: Path to the text file for knowledge graph extraction
- `--ontology_json`: Path to the ontology JSON file
- `--ontology_owl`: Path to the ontology OWL file
- `--server_job_paths`: Path to the server's job output directory (for accessing server-side files)

Available modes:
- `run`: Create and run a text-to-KG job
- `list`: List all jobs
- `retry`: Retry a failed job
- `delete`: Delete a job

For help and all available options:

```bash
text-to-kg --help
```

## Configuration

### Client Configuration

The client can be configured with the following parameters:

- `base_url`: URL of the CleverSwarm API server (required)
- `username`: Username for authentication (can be prompted if not provided)
- `token`: Authentication token (can be generated via `update_token()`)
- `timeout`: Request timeout in seconds (default: 30)
- `verify_ssl`: Whether to verify SSL certificates (default: True)

### Server Configuration

The server requires the following configuration:

1. Ensure the server has access to necessary resources:
   - Processing engines
   - Storage for job outputs
   - Authentication database

2. Configure server directories:
   - Input directory: Where uploaded files are stored
   - Output directory: Where job results are stored
   - Log directory: For server logs

3. Set up environment variables (if required by your server):
   ```bash
   export CLEVERSWARM_LOG_LEVEL=INFO
   export CLEVERSWARM_DATA_DIR=/path/to/data
   ```

## Troubleshooting

Common issues and solutions:

1. **Connection refused**: Ensure the REST API server is running and accessible
2. **Authentication failed**: Check username and token or regenerate token
3. **File not found**: Verify file paths and permissions
4. **Job processing errors**: Check server logs for details

## Documentation

The client library provides the following main classes:

- `CleverSwarmClient`: Core client for interacting with the CleverSwarm API
- `TextToKGCLI`: Command-line interface for text-to-KG operations

### CleverSwarmClient Methods

- `get_jobs_list(is_benchmark=False)`: Get a list of jobs
- `get_job_status(job_id)`: Get the status of a job
- `get_job_details(job_id)`: Get detailed information about a job
- `create_unstructured_to_kg_job(unstructured_text_file, ontology_file, ontology_spec_file, force_filetype=FileTypeAPI.AutoDetect)`: Create a text-to-KG job
- `create_unstructured_to_kg_wildcards_job(unstructured_text_file, ontology_file, ontology_spec_file, wildcards_query_file, force_filetype=FileTypeAPI.AutoDetect)`: Create a text-to-KG job with wildcards
- `retrieve_unstructured_to_kg_files(job_id, output_filepath)`: Download the results of a text-to-KG job
- `delete_job(job_id)`: Delete a job
- `retry_job(job_id)`: Retry a failed job

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 