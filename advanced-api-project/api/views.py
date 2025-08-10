# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# LIST all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # anyone can read, only logged-in can create


# DETAIL view (will expect ?id= query parameter)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        book_id = self.request.query_params.get("id")
        return generics.get_object_or_404(Book, id=book_id)


# CREATE a book
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in can create


# UPDATE a book (will expect ID in request data)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in can update

    def get_object(self):
        book_id = self.request.data.get("id")
        return generics.get_object_or_404(Book, id=book_id)


# DELETE a book (will expect ID in request data)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in can delete

    def get_object(self):
        book_id = self.request.data.get("id")
        return generics.get_object_or_404(Book, id=book_id)
