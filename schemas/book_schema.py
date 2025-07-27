"""
Book schema for data serialization and validation.
"""

from datetime import datetime
from typing import Dict, Any, Optional

class BookSchema:
    """Book data schema and serialization"""
    
    @staticmethod
    def serialize(book: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize a book object for API response"""
        return {
            "id": book.get("id"),
            "title": book.get("title"),
            "author": book.get("author"),
            "year": book.get("year"),
            "genre": book.get("genre"),
            "description": book.get("description", ""),
            "created_at": book.get("created_at"),
            "updated_at": book.get("updated_at")
        }
    
    @staticmethod
    def serialize_list(books: list) -> list:
        """Serialize a list of books"""
        return [BookSchema.serialize(book) for book in books]
    
    @staticmethod
    def deserialize(data: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize and clean book data from request"""
        return {
            "title": data.get("title", "").strip() if data.get("title") else None,
            "author": data.get("author", "").strip() if data.get("author") else None,
            "year": data.get("year"),
            "genre": data.get("genre", "").strip() if data.get("genre") else None,
            "description": data.get("description", "").strip() if data.get("description") else ""
        }
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate required fields for book creation"""
        required_fields = ['title', 'author']
        for field in required_fields:
            if not data.get(field):
                return False, f"Missing required field: {field}"
        return True, ""
    
    @staticmethod
    def get_book_summary(book: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of book information"""
        return {
            "id": book.get("id"),
            "title": book.get("title"),
            "author": book.get("author"),
            "year": book.get("year"),
            "genre": book.get("genre")
        } 