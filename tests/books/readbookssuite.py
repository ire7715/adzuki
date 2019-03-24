from datetime import datetime, timezone
from google.cloud import datastore
from tests.books import AbstractTestBook, Book

class ReadBooksSuite(AbstractTestBook):
  def setUp(self):
    self._ISBN = '978-0618968633'
    self._entity = {
      'title': 'The Hobbit',
      'language': 'English',
      'pages': 320,
      'author': {
        'name': 'J.R.R. Tolkien'
      },
      'released_at': datetime(2007, 9, 17, tzinfo=timezone.utc)
    }
    raw_book_entity = datastore.Entity(key=self._client.key(self._kind, self._ISBN))
    for key, value in self._entity.items():
      raw_book_entity[key] = value
    self._client.put(raw_book_entity)

  def tearDown(self):
    key = self._client.key(self._kind, self._ISBN)
    self._client.delete(key)

  def testGetBook(self):
    books_model = Book()
    book_entity = books_model.get(self._ISBN)
    self.assertEqual(book_entity.id, self._ISBN)
    for key, value in self._entity.items():
      self.assertEqual(book_entity[key], value)
