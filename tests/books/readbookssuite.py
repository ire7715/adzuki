from datetime import datetime, timezone
from google.cloud import datastore
from tests.books import AbstractTestBook, Book

class ReadBooksSuite(AbstractTestBook):
  def setUp(self):
    self._entities = {
      '978-0618968633': {
        'title': 'The Hobbit',
        'language': 'English',
        'pages': 320,
        'author': {
          'name': 'J.R.R. Tolkien'
        },
        'released_at': datetime(2007, 9, 17, tzinfo=timezone.utc)
      },
      '978-0375823732': {
        'title': 'The Hobbit',
        'language': 'English',
        'pages': 320,
        'author': {
          'name': 'J.R.R. Tolkien'
        },
        'released_at': datetime(2007, 9, 17, tzinfo=timezone.utc)
      },
      '978-1328557513': {
        'title': 'A Middle-earth Traveler: Sketches from Bag End to Mordor',
        'language': 'English',
        'pages': 176,
        'author': {
          'name': 'John Howe'
        },
        'released_at': datetime(2018, 10, 9, tzinfo=timezone.utc)
      }
    }
    for isbn, entity in self._entities.items():
      raw_book_entity = datastore.Entity(key=self._client.key(self._kind, isbn))
      for key, value in entity.items():
        raw_book_entity[key] = value
      self._client.put(raw_book_entity)

  def tearDown(self):
    for isbn, entity in self._entities.items():
      key = self._client.key(self._kind, isbn)
      self._client.delete(key)

  def testGetBook(self):
    expected_isbn, expected_entity = next(iter(self._entities.items()))

    books_model = Book()
    book_entity = books_model.get(expected_isbn)
    self.assertEqual(book_entity.id, expected_isbn)
    for key, value in expected_entity.items():
      self.assertEqual(book_entity[key], value)
