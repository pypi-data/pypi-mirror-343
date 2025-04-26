# API Reference

This document provides detailed documentation for Elastro's core components and their methods.

## Table of Contents

- [ElasticsearchClient](#elasticsearchclient)
- [IndexManager](#indexmanager)
- [DocumentManager](#documentmanager)
- [DatastreamManager](#datastreammanager)
- [Advanced Components](#advanced-components)
  - [QueryBuilder](#querybuilder)
  - [AggregationBuilder](#aggregationbuilder)
  - [ScrollHelper](#scrollhelper)

## ElasticsearchClient

The `ElasticsearchClient` class is the primary entry point for connecting to Elasticsearch.

### Constructor

```python
client = ElasticsearchClient(
    hosts=None,  # List of Elasticsearch hostnames/IPs
    auth=None,   # Authentication details
    timeout=30,  # Connection timeout in seconds
    retry_on_timeout=True,  # Whether to retry on timeout
    max_retries=3,  # Maximum number of retries
    profile=None  # Configuration profile to use
)
```

### Methods

#### `connect()`

Establishes a connection to the Elasticsearch cluster.

```python
client.connect()
```

#### `health()`

Retrieves health information about the Elasticsearch cluster.

```python
health = client.health()
# Returns: Dict with cluster health status
```

#### `indices()`

Lists all indices in the cluster.

```python
indices = client.indices()
# Returns: List of index names
```

## IndexManager

The `IndexManager` class handles operations related to Elasticsearch indices.

### Constructor

```python
index_manager = IndexManager(client)
```

### Methods

#### `create(name, settings=None, mappings=None)`

Creates a new index with optional settings and mappings.

```python
result = index_manager.create(
    name="my-index",
    settings={
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
    mappings={
        "properties": {
            "field1": {"type": "text"},
            "field2": {"type": "keyword"}
        }
    }
)
# Returns: Dict with creation result
```

#### `get(name)`

Retrieves information about an index.

```python
info = index_manager.get("my-index")
# Returns: Dict with index information
```

#### `exists(name)`

Checks if an index exists.

```python
exists = index_manager.exists("my-index")
# Returns: Boolean
```

#### `update(name, settings)`

Updates settings for an existing index.

```python
result = index_manager.update(
    "my-index",
    {"index": {"number_of_replicas": 2}}
)
# Returns: Dict with update result
```

#### `delete(name)`

Deletes an index.

```python
result = index_manager.delete("my-index")
# Returns: Dict with deletion result
```

#### `open(name)`

Opens a closed index.

```python
result = index_manager.open("my-index")
# Returns: Dict with operation result
```

#### `close(name)`

Closes an open index.

```python
result = index_manager.close("my-index")
# Returns: Dict with operation result
```

## DocumentManager

The `DocumentManager` class handles document operations.

### Constructor

```python
doc_manager = DocumentManager(client)
```

### Methods

#### `index(index, id, document)`

Indexes a document with the given ID.

```python
result = doc_manager.index(
    index="my-index",
    id="doc-1",
    document={"field1": "value1", "field2": "value2"}
)
# Returns: Dict with indexing result
```

#### `bulk_index(index, documents)`

Indexes multiple documents in a single operation.

```python
documents = [
    {"id": "doc-1", "document": {"field1": "value1"}},
    {"id": "doc-2", "document": {"field1": "value2"}}
]
result = doc_manager.bulk_index("my-index", documents)
# Returns: Dict with bulk indexing result
```

#### `get(index, id)`

Retrieves a document by ID.

```python
document = doc_manager.get("my-index", "doc-1")
# Returns: Dict with document
```

## Advanced Components

### QueryBuilder

The `QueryBuilder` class helps to construct complex Elasticsearch queries.

```python
from elastro.advanced import QueryBuilder

// ... existing code ...
```

### AggregationBuilder

The `AggregationBuilder` class helps to construct Elasticsearch aggregations.

```python
from elastro.advanced import AggregationBuilder

// ... existing code ...
```

### ScrollHelper

The `ScrollHelper` class helps with scrolling through large result sets.

```python
from elastro.advanced import ScrollHelper
from elastro import ElasticsearchClient

// ... existing code ...
```