# Elastro

A comprehensive Python module for managing Elasticsearch operations within pipeline processes.

## Overview

Elastro is a Python library designed to simplify interactions with Elasticsearch. It provides a clean, intuitive API for common Elasticsearch operations including:

- Index management (create, update, delete)
- Document operations (indexing, searching, updating)
- Datastream management
- Advanced query building and search functionality

The library offers both a programmatic API and a command-line interface for seamless integration with various workflows.

## Installation

```bash
pip install elastro
```

Or from source:

```bash
git clone https://github.com/Fremen-Labs/elastro.git
cd elastro
pip install -e .
```

## Basic Usage

### Client Connection

```python
from elastro import ElasticsearchClient

# Connect using API key
client = ElasticsearchClient(
    hosts=["https://elasticsearch:9200"],
    auth={"api_key": "your-api-key"}
)

# Or using basic auth
client = ElasticsearchClient(
    hosts=["https://elasticsearch:9200"],
    auth={"username": "elastic", "password": "password"}
)

# Connect to Elasticsearch
client.connect()
```

### Index Management

```python
from elastro import IndexManager

index_manager = IndexManager(client)

# Create an index
index_manager.create(
    name="products",
    settings={
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    mappings={
        "properties": {
            "name": {"type": "text"},
            "price": {"type": "float"},
            "description": {"type": "text"},
            "created": {"type": "date"}
        }
    }
)

# Check if an index exists
if index_manager.exists("products"):
    print("Products index exists!")
    
# Delete an index
index_manager.delete("products")
```

### Document Operations

```python
from elastro import DocumentManager

doc_manager = DocumentManager(client)

# Index a document
doc_manager.index(
    index="products",
    id="1",
    document={
        "name": "Laptop",
        "price": 999.99,
        "description": "High-performance laptop",
        "created": "2023-05-01T12:00:00"
    }
)

# Search for documents
results = doc_manager.search(
    index="products",
    query={"match": {"name": "laptop"}}
)

print(results)
```

### CLI Usage

```bash
# Initialize configuration
elastic-cli config init

# Create an index
elastic-cli index create products --shards 3 --replicas 1 --mapping ./product-mapping.json

# Add a document
elastic-cli doc index products --id 1 --file ./product.json

# Search documents
elastic-cli search products "name:laptop" --format json
```

## Documentation

For more detailed documentation, please refer to the [docs](https://github.com/Fremen-Labs/elastro/tree/main/docs) directory:

- [Getting Started](https://github.com/Fremen-Labs/elastro/blob/main/docs/getting_started.md)
- [API Reference](https://github.com/Fremen-Labs/elastro/blob/main/docs/api_reference.md)
- [CLI Usage](https://github.com/Fremen-Labs/elastro/blob/main/docs/cli_usage.md)
- [Advanced Features](https://github.com/Fremen-Labs/elastro/blob/main/docs/advanced_features.md)
- [Troubleshooting](https://github.com/Fremen-Labs/elastro/blob/main/docs/troubleshooting.md)

## Examples

Check out the [examples](https://github.com/Fremen-Labs/elastro/tree/main/examples) directory for more usage examples:

- [Client Connection](https://github.com/Fremen-Labs/elastro/blob/main/examples/client.py)
- [Index Management](https://github.com/Fremen-Labs/elastro/blob/main/examples/index_management.py)
- [Document Operations](https://github.com/Fremen-Labs/elastro/blob/main/examples/document_operations.py)
- [Search Operations](https://github.com/Fremen-Labs/elastro/blob/main/examples/search.py)
- [Datastream Management](https://github.com/Fremen-Labs/elastro/blob/main/examples/datastreams.py)

## Contributing

We welcome contributions to Elastro! If you'd like to contribute, please follow these guidelines:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/elastro.git`
3. Install development dependencies: `pip install -e ".[dev]"`
4. Create a branch for your changes: `git checkout -b feature/your-feature-name`

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints for all method signatures and return values
- Write comprehensive docstrings (PEP 257) for all public classes and methods
- Keep files under 300 lines of code maximum
- Implement custom exception classes for different error categories
- Validate inputs using Pydantic before processing

### Architecture Guidelines

- Maintain separation of concerns between core functionality and interfaces
- Design modular components with single responsibilities
- Follow SOLID principles
- Implement dependency injection for better testability
- Structure code by functionality rather than technology type

### Testing

- Write unit tests with pytest for all new functionality
- Maintain test coverage of at least 80% for core functionality
- Run tests using `./run_tests.sh` before submitting a PR

### Submitting Changes

1. Ensure your code follows the project's standards
2. Write meaningful commit messages
3. Push your changes to your fork
4. Submit a pull request to the main repository
5. Describe your changes and the problem they solve

### Documentation

- Update documentation for any changed functionality
- Add examples for new features
- Write clear, concise docstrings for all public APIs

## License

MIT 