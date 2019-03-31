from datetime import datetime, timezone
from google.cloud import datastore
from tests.books import AbstractTestBook, Book

class BooksOperationSuite(AbstractTestBook):
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
        'title': 'Bilbo\'s Last Song',
        'language': 'English',
        'pages': 32,
        'author': {
          'name': 'J.R.R. Tolkien'
        },
        'released_at': datetime(2002, 9, 24, tzinfo=timezone.utc)
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

  def testQueryBooks(self):
    postprojection = ['title', 'pages']
    book_model = Book()
    entities = book_model.query(filters=[
      ('auther.name', '=', 'J.R.R. Tolkien')
    ], postprojection=postprojection)

    for entity in entities:
      self.assertTrue(entity.id in self._entities)
      expected_entity = self._entities[entity.id]
      for key in postprojection:
        self.assertEqual(entity[key], expected_entity[key])
      self.assertEqual(entity['language'], None)

  def testEditBook(self):
    isbn, _ = next(iter(self._entities.items()))
    expected_title = 'Foo'
    expected_author_name = 'Bar'

    books_model = Book()
    book_entity = books_model.get(isbn)
    book_entity['title'] = expected_title
    book_entity['author']['name'] = expected_author_name
    book_entity.put()
    updated_entity = books_model.get(isbn)
    self.assertEqual(updated_entity['title'], expected_title)
    self.assertEqual(updated_entity['author']['name'], expected_author_name)

  def testEditViolation(self):
    isbn, _ = next(iter(self._entities.items()))

    books_model = Book()
    book_entity = books_model.get(isbn)
    with self.assertRaises(Exception):
      book_entity['pages'] = 'three twenty'
