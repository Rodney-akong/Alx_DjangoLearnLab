# api/views.py
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# LIST + CREATE
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    # anyone can read, only logged-in can create

# RETRIEVE (single book) + UPDATE + DELETE
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    # read for all, modify for logged-in users
