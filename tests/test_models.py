"""
Tests for the models.
"""

import unittest
import tempfile
import os
import json
from models.book import Book
from models.author import Author
from config import TestingConfig

class TestBookModel(unittest.TestCase):
    """Test cases for Book model"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = TestingConfig()
        self.book_model = Book(self.config)
    
    def test_create_book(self):
        """Test creating a new book"""
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "genre": "Test",
            "description": "A test book"
        }
        
        result = self.book_model.create_book(book_data)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["title"], "Test Book")
        self.assertEqual(result["data"]["author"], "Test Author")
    
    def test_get_book_by_id(self):
        """Test getting a book by ID"""
        # First create a book
        book_data = {
            "title": "Test Book",
            "author": "Test Author"
        }
        create_result = self.book_model.create_book(book_data)
        book_id = create_result["data"]["id"]
        
        # Then get it by ID
        result = self.book_model.get_book_by_id(book_id)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["id"], book_id)
    
    def test_get_nonexistent_book(self):
        """Test getting a book that doesn't exist"""
        result = self.book_model.get_book_by_id(999)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Book not found")
    
    def test_validate_book_data(self):
        """Test book data validation"""
        # Test missing required fields
        invalid_data = {"title": "Test Book"}  # Missing author
        is_valid, error_msg = self.book_model._validate_book_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("author", error_msg)
        
        # Test valid data
        valid_data = {
            "title": "Test Book",
            "author": "Test Author"
        }
        is_valid, error_msg = self.book_model._validate_book_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

class TestAuthorModel(unittest.TestCase):
    """Test cases for Author model"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = TestingConfig()
        self.author_model = Author(self.config)
    
    def test_create_author(self):
        """Test creating a new author"""
        author_data = {
            "name": "Test Author",
            "birth_year": 1990,
            "nationality": "Test",
            "biography": "A test author"
        }
        
        result = self.author_model.create_author(author_data)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["name"], "Test Author")
    
    def test_get_author_by_id(self):
        """Test getting an author by ID"""
        # First create an author
        author_data = {"name": "Test Author"}
        create_result = self.author_model.create_author(author_data)
        author_id = create_result["data"]["id"]
        
        # Then get it by ID
        result = self.author_model.get_author_by_id(author_id)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["id"], author_id)
    
    def test_validate_author_data(self):
        """Test author data validation"""
        # Test missing required fields
        invalid_data = {}  # Missing name
        is_valid, error_msg = self.author_model._validate_author_data(invalid_data)
        self.assertFalse(is_valid)
        self.assertIn("name", error_msg)
        
        # Test valid data
        valid_data = {"name": "Test Author"}
        is_valid, error_msg = self.author_model._validate_author_data(valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

if __name__ == '__main__':
    unittest.main() 