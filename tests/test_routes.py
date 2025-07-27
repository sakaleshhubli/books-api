"""
Tests for the routes.
"""

import unittest
import json
from app import create_app
from config import TestingConfig

class TestBookRoutes(unittest.TestCase):
    """Test cases for book routes"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_get_books(self):
        """Test getting all books"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("pagination", data)
    
    def test_create_book(self):
        """Test creating a new book"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "genre": "Test"
        }
        
        response = self.client.post(
            '/api/books/',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["title"], "Test Book")
        self.assertEqual(data["data"]["author"], "Test Author")
    
    def test_create_book_missing_fields(self):
        """Test creating a book with missing required fields"""
        book_data = {"title": "Test Book"}  # Missing author
        
        response = self.client.post(
            '/api/books/',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertIn("author", data["error"])
    
    def test_get_book_by_id(self):
        """Test getting a book by ID"""
        # First create a book
        book_data = {
            "title": "Test Book",
            "author": "Test Author"
        }
        
        create_response = self.client.post(
            '/api/books/',
            data=json.dumps(book_data),
            content_type='application/json'
        )
        
        create_data = json.loads(create_response.data)
        book_id = create_data["data"]["id"]
        
        # Then get it by ID
        response = self.client.get(f'/api/books/{book_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], book_id)
    
    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist"""
        response = self.client.get('/api/books/999')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Book not found")
    
    def test_search_books(self):
        """Test searching books"""
        response = self.client.get('/api/books/search?q=test')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        self.assertIn("query", data)

class TestAuthorRoutes(unittest.TestCase):
    """Test cases for author routes"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_get_authors(self):
        """Test getting all authors"""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertIn("data", data)
    
    def test_create_author(self):
        """Test creating a new author"""
        author_data = {
            "name": "Test Author",
            "birth_year": 1990,
            "nationality": "Test"
        }
        
        response = self.client.post(
            '/api/authors/',
            data=json.dumps(author_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["name"], "Test Author")

class TestGeneralRoutes(unittest.TestCase):
    """Test cases for general routes"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn("message", data)
        self.assertIn("endpoints", data)
        self.assertIn("version", data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
    
    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], "Endpoint not found")

if __name__ == '__main__':
    unittest.main() 