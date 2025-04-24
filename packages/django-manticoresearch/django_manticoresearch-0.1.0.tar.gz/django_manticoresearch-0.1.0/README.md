# Django Manticoresearch

Django integration for Manticore Search engine.

## Installation

```bash
pip install django-manticoresearch
```

## Configuration

Add `django_manticoresearch` to your `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    # ...
    'django_manticoresearch',
    # ...
]
```

Configure Manticore connection settings:

```python
MANTICORE_SCHEMA = "http"
MANTICORE_HOST = "localhost"
MANTICORE_PORT = 9308
```

## Basic Usage

### Define Indices (Legacy API)

This style uses class attributes for field definitions and a Meta class for configuration. This is fully supported for backward compatibility.

```python
from django_manticoresearch import ManticoreIndex, CharField, IntegerField

class PostIndex(ManticoreIndex):
    title = CharField()
    content = CharField()
    views = IntegerField()
    
    class Meta:
        index_name = 'posts'
        model = YourModel  # Optional, can also be set during initialization
```

### Define Indices (New Advanced API)

The new style uses a more explicit approach with fields defined as a tuple:

```python
from django_manticoresearch import BaseManticoreIndex, TextField, BigintField, index_registry
from myapp.models import Post

@index_registry.register
class PostIndex(BaseManticoreIndex):
    _index_name = "posts"
    model = Post
    
    fields = (
        TextField("title"),
        TextField("content"),
        BigintField("views"),
    )
    
    # Optional field weights for relevance scoring
    field_weights = {
        "title": 10,
        "content": 5,
    }
```

## Searching with Different APIs

### Legacy API

```python
# Class method approach
results = PostIndex.search("query text")

# Convert to Django queryset
queryset = PostIndex.model.objects.filter(id__in=[hit["_id"] for hit in results])
```

### New API

```python
# Initialize the index
index = PostIndex()

# Basic search
results = index.search("query text")

# Advanced search with options
results = index.search(
    query="query text",
    match_fields=["title", "content"],
    enable_wildcard_search=True,
    infix_search=True
)

# Convert results to Django QuerySet
queryset = index.search_result_to_queryset(results)
```

## Auto-Indexing

The package automatically connects signals to update indices when model instances are created, updated, or deleted.

## Management Commands

Create all indices:

```bash
python manage.py manticore_setup_indexes
```

Create indices for a specific app:

```bash
python manage.py manticore_setup_indexes --app=myapp
```

Create indices and index all objects:

```bash
python manage.py manticore_setup_indexes --reindex
```

Drop existing indices before creating:

```bash
python manage.py manticore_setup_indexes --recreate
```

## Features

- Django ORM-like interface for Manticore search
- Advanced search with wildcards, prefix, infix and full-text search
- Automatic index management with Django signals
- Field type validation and transformation
- Rich query builder API
- Highlighting support
- Support for complex data structures 