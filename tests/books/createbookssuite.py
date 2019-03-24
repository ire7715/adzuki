from tests.books import Book
from datetime import datetime, timezone
from tests.books import AbstractTestBook

class CreateBooksSuite(AbstractTestBook):
  def setUp(self):
    self._ISBN = '978-0618968633'

  def tearDown(self):
    key = self._client.key(self._kind, self._ISBN)
    self._client.delete(key)

  def testCreate(self):
    expected_book_entity = {
      'title': 'The Hobbit',
      'language': 'English',
      'pages': 320,
      'author': {
        'name': 'J.R.R. Tolkien'
      },
      'released_at': datetime(2007, 9, 17, tzinfo=timezone.utc)
    }

    books_model = Book()
    book_handler = books_model.create(self._ISBN)
    for key, value in expected_book_entity.items():
      book_handler[key] = value
    book_handler.put()

    book_entity = books_model.get(self._ISBN)
    self.assertEqual(book_entity.id, self._ISBN)
    for key, value in expected_book_entity.items():
      self.assertEqual(book_entity[key], value)

  def testCreateWrongSchema(self):
    input_entity = {
      'title': 'The Hobbit',
      'language': 'English',
      'pages': '320',
      'author.name': 'J.R.R. Tolkien',
      'released_at': '2007-09-17T00:00:00Z'
    }

    books_model = Book()
    book_handler = books_model.create(self._ISBN)
    for key, value in input_entity.items():
      if key in ['author.name', 'released_at']:
        with self.assertRaises(Exception):
          book_handler[key] = value
      else:
        book_handler[key] = value
    book_handler.put()

    book_entity = books_model.get(self._ISBN)
    self.assertEqual(book_entity.id, self._ISBN)
    for key, value in input_entity.items():
      if key in ['author.name', 'released_at']:
        continue
      elif key == 'pages':
        self.assertEqual(book_entity[key], int(value))
      else:
        self.assertEqual(book_entity[key], value)
