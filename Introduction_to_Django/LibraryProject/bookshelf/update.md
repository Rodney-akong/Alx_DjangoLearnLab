
book = Book.objects.get(title="1984"); 
book.title = "Nineteen Eighty-Four"; 
book.save()
Output: Title updated successfully