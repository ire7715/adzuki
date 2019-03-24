from google.cloud import datastore
import configparser, os, unittest

class AbstractTestBook(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(AbstractTestBook, self).__init__(*args, **kwargs)
    source_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../')
    self._config = configparser.ConfigParser()
    self._config.read(os.path.join(source_path, 'config/config.cfg'))
    self._project = self._config.get('books', 'project')
    self._namespace = self._config.get('books', 'namespace')
    self._kind = self._config.get('books', 'kind')
    self._client = datastore.Client(project=self._project, namespace=self._namespace)
