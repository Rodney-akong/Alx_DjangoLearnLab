from django.db import models

# Create your models here.
from django.db import models
from datetime import date

# Author model: represents a single author
class Author(models.Model):
    name = models.CharField(max_length=100)  # Author's full name

    def __str__(self):
        return self.name  # Show name in admin panel & queries


# Book model: represents a book written by an Author
class Book(models.Model):
    title = models.CharField(max_length=200)           # Book title
    publication_year = models.IntegerField()           # Year book was published
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    # related_name='books' lets us access author.books to get all books for that author

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
