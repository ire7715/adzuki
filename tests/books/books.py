from adzuki import Model
from datetime import datetime
import configparser

class Book(Model):
  def __init__(self, *args, **kwargs):
    self._config = configparser.ConfigParser()
    self._config.read('config/config.cfg')
    self._project = self._config.get('books', 'project')
    self._namespace = self._config.get('books', 'namespace')
    self._kind = self._config.get('books', 'kind')
    super(Book, self).__init__(*args, **kwargs)

  @property
  def project(self):
    return self._project

  @property
  def namespace(self):
    return self._namespace

  @property
  def kind(self):
    return self._kind

  @property
  def schema(self):
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
