# api/test_views.py
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date

from .models import Book

User = get_user_model()


class BookAPITestCase(TestCase):
    def setUp(self):
        # Test client
        self.client = APIClient()

        # Create a user for authenticated actions
        self.user = User.objects.create_user(username="tester", password="testpass123")

        # Create several book instances with varying data
        self.book1 = Book.objects.create(
            title="Django for APIs",
            author="William Vincent",
            published_date=date(2020, 3, 1),
            isbn="1111111111111",
            pages=200,
        )
        self.book2 = Book.objects.create(
            title="Two Scoops of Django",
            author="Daniel Roy Greenfeld",
            published_date=date(2019, 6, 15),
            isbn="2222222222222",
            pages=350,
        )
        self.book3 = Book.objects.create(
            title="Learn Python the Hard Way",
            author="Zed Shaw",
            published_date=date(2013, 10, 1),
            isbn="3333333333333",
            pages=300,
        )

        # Paths used by tests (adjust if your URL prefix differs)
        self.list_url = "/books/"
        self.create_url = "/books/create/"
        self.update_url = "/books/update/"
        self.delete_url = "/books/delete/"
        self.detail_url = "/books/detail/"  # if used (expects ?id=)
    
    def test_list_books_anonymous_allowed(self):
        """Anyone (anonymous) should be able to list books (IsAuthenticatedOrReadOnly)."""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Expect at least the three books created in setUp
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_create_book_requires_auth(self):
        """POST to create without auth should be rejected; with auth should succeed."""
        data = {
            "title": "New Book",
            "author": "Author X",
            "published_date": "2024-01-01",
            "isbn": "4444444444444",
            "pages": 150,
        }

        # Unauthenticated attempt
        resp_unauth = self.client.post(self.create_url, data, format="json")
        self.assertIn(resp_unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticated attempt
        self.client.force_authenticate(user=self.user)
        resp_auth = self.client.post(self.create_url, data, format="json")
        self.assertEqual(resp_auth.status_code, status.HTTP_201_CREATED)
        created = resp_auth.json()
        self.assertEqual(created.get("title"), data["title"])
        # Clean up auth state for other tests
        self.client.force_authenticate(user=None)

    def test_update_book_requires_auth_and_updates_fields(self):
        """Updating a book requires auth and actually changes the DB entry."""
        update_payload = {
            "id": self.book1.id,
            "title": "Django for APIs - 2nd Edition",
        }

        # Unauthenticated -> should be rejected
        resp_unauth = self.client.patch(self.update_url, update_payload, format="json")
        self.assertIn(resp_unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticated -> succeeds
        self.client.force_authenticate(user=self.user)
        resp_auth = self.client.patch(self.update_url, update_payload, format="json")
        # Depending on your UpdateAPIView, status may be 200 OK or 202/204. We accept 200 or 204/202/201.
        self.assertIn(resp_auth.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED, status.HTTP_204_NO_CONTENT))
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, update_payload["title"])
        self.client.force_authenticate(user=None)

    def test_delete_book_requires_auth_and_removes_record(self):
        """Deleting a book requires auth; successful delete removes book."""
        payload = {"id": self.book2.id}

        # Unauthenticated -> rejected
        resp_unauth = self.client.delete(self.delete_url, payload, format="json")
        self.assertIn(resp_unauth.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticated -> success and record removed
        self.client.force_authenticate(user=self.user)
        resp_auth = self.client.delete(self.delete_url, payload, format="json")
        # Accept typical delete responses
        self.assertIn(resp_auth.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        # Ensure it no longer exists
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(id=self.book2.id)
        self.client.force_authenticate(user=None)

    def test_search_by_title_or_author(self):
        """Search filter should return items matching title or author (search param)."""
        # search for "django"
        resp = self.client.get(f"{self.list_url}?search=django")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        # book1 ("Django for APIs") should be in results
        titles = [r.get("title") for r in results]
        self.assertTrue(any("Django" in t for t in titles))

        # search for author "Zed"
        resp2 = self.client.get(f"{self.list_url}?search=zed")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        results2 = resp2.json()
        self.assertTrue(any("Zed" in r.get("author", "") for r in results2))

    def test_ordering_by_published_date(self):
        """Ordering works: newest first when ordering=-published_date."""
        resp = self.client.get(f"{self.list_url}?ordering=-published_date")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        # convert published_date strings to comparable values if present
        dates = [r.get("published_date") for r in results if r.get("published_date")]
        self.assertTrue(len(dates) >= 3)
        # Check that first date is >= second date (newest first)
        self.assertGreaterEqual(dates[0], dates[1])

    def test_filter_by_publication_year(self):
        """Filter results by publication_year (expects filter to exist)."""
        # Created books: 2020, 2019, 2013
        resp_2020 = self.client.get(f"{self.list_url}?publication_year=2020")
        self.assertEqual(resp_2020.status_code, status.HTTP_200_OK)
        results_2020 = resp_2020.json()
        # Only book1 should appear
        self.assertTrue(any(r.get("title") == self.book1.title for r in results_2020))
        # Ensure non-2020 not present
        self.assertFalse(any(r.get("title") == self.book2.title for r in results_2020))

