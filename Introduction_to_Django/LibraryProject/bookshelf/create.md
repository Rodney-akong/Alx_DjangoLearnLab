## Create Operation

from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# A Book object is created successfully

book.id # e.g., returns: 1