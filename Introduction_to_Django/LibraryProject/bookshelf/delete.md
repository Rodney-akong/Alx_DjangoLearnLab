book = Book.objects.get(title="Nineteen Eighty-Four"); 
book.delete()
Output: Book instance deleted successfully. `Book.objects.all()` returns an empty queryset.

