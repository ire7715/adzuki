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
  def attributes(self):
    return {
      'title': str,
      'language': str,
      'pages': int,
      'author': {
        'name': str
      },
      'released_at': datetime
    }
