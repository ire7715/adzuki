# Adzuki
Adzuki is an ORM of Google Cloud Datastore.

## Quick start
### Define your model
```python
from adzuki import Model

class Book(Model):
  @property
  def project(self):
    return 'random-project-12345' # put your GCP project ID here

  @property
  def namespace(self):
    return 'Library' # put the namespace of your dataset here

  @property
  def kind(self):
    return 'Book' # Kind of this dataset

  @property
  def schema(self):
    # Adzuki supports json schema definition
    return {
      '$schema': 'http://json-schema.org/draft-07/schema#',
      'title': 'Book example for Adzuki',
      'description': '',
      'required': [ 'title', 'author', 'released_at' ],
      'type': 'object',
      'properties': {
        'title': { 'type': 'string' },
        'language': { 'type': 'string' },
        'pages': { 'type': 'number' },
        'author': {
          'type': 'object',
          'required': [ 'name' ],
          'properties': {
            'name': { 'type': 'string' }
          }
        },
        'released_at': { 'type': 'datetime' }
      }
    }
```

### Entity creation
```python
from datetime import datetime

book_model = Book()
book_entity = books_model.create('978-0618968633')
book_entity['title'] = 'The Hobbit'
book_entity['author'] = 'J.R.R. Tolkien'
book_entity['released_at'] = datetime(2007, 9, 17, tzinfo=timezone.utc)
book_entity.put()
```

### Entities query
```python
entities = book_model.query(filters=[
  ('auther.name', '=', 'J.R.R. Tolkien')
])
for entity in entities:
  print(dict(entity))
```

### Entity editing
```python
entity = book_model.get('978-0618968633')
entity['language'] = 'English'
entity.put()
```
