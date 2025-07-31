from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Optional list-only view
    path('auth/token/', obtain_auth_token, name='api-token'),  # 🔑 Token login endpoint
    path('', include(router.urls)),  # ViewSet CRUD endpoints
]