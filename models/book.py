"""
Book model and data operations.
Handles all book-related data operations including CRUD operations.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from config import Config

class Book:
    """Book model and data operations"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.books = self._load_books()
    
    def _load_books(self) -> List[Dict[str, Any]]:
        """Load books from JSON file"""
        if os.path.exists(self.config.BOOKS_FILE):
            try:
                with open(self.config.BOOKS_FILE, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        return data
                    else:
                        print("Invalid JSON structure, using default books")
                        return self._get_default_books()
            except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
                print(f"Error loading books: {e}")
                return self._get_default_books()
        else:
            # Create file with default books
            default_books = self._get_default_books()
            self._save_books(default_books)
            return default_books
    
    def _save_books(self, books_data: List[Dict[str, Any]]) -> bool:
        """Save books to JSON file"""
        try:
            with open(self.config.BOOKS_FILE, 'w', encoding='utf-8') as file:
                json.dump(books_data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving books to file: {e}")
            return False
    
    def _get_default_books(self) -> List[Dict[str, Any]]:
        """Load default books from external JSON file"""
        try:
            if os.path.exists(self.config.DEFAULT_BOOKS_FILE):
                with open(self.config.DEFAULT_BOOKS_FILE, 'r', encoding='utf-8') as file:
                    default_books = json.load(file)
                    if isinstance(default_books, list):
                        return default_books
                    else:
                        print("Invalid default books JSON structure")
                        return self._get_fallback_books()
            else:
                print(f"Default books file not found: {self.config.DEFAULT_BOOKS_FILE}")
                return self._get_fallback_books()
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading default books: {e}")
            return self._get_fallback_books()
    
    def _get_fallback_books(self) -> List[Dict[str, Any]]:
        """Return minimal fallback books if default file fails"""
        return [
            {
                "id": 1,
                "title": "Sample Book",
                "author": "Sample Author",
                "year": 2023,
                "genre": "Fiction",
                "description": "A sample book for testing purposes."
            }
        ]
    
    def _validate_book_data(self, data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, str]:
        """Validate book data"""
        if not isinstance(data, dict):
            return False, "Invalid data format"
        
        # Required fields for creation
        if not is_update:
            required_fields = ['title', 'author']
            for field in required_fields:
                if field not in data or not data[field]:
                    return False, f"Missing required field: {field}"
        
        # Validate title
        if 'title' in data:
            title = str(data['title']).strip()
            if not title:
                return False, "Title cannot be empty"
            if len(title) > self.config.MAX_TITLE_LENGTH:
                return False, f"Title too long (max {self.config.MAX_TITLE_LENGTH} characters)"
        
        # Validate author
        if 'author' in data:
            author = str(data['author']).strip()
            if not author:
                return False, "Author cannot be empty"
            if len(author) > self.config.MAX_AUTHOR_LENGTH:
                return False, f"Author name too long (max {self.config.MAX_AUTHOR_LENGTH} characters)"
        
        # Validate year
        if 'year' in data and data['year'] is not None:
            try:
                year = int(data['year'])
                if year < self.config.MIN_YEAR or year > self.config.MAX_YEAR:
                    return False, f"Year must be between {self.config.MIN_YEAR} and {self.config.MAX_YEAR}"
            except (ValueError, TypeError):
                return False, "Year must be a valid integer"
        
        # Validate genre
        if 'genre' in data and data['genre'] is not None:
            genre = str(data['genre']).strip()
            if len(genre) > self.config.MAX_GENRE_LENGTH:
                return False, f"Genre too long (max {self.config.MAX_GENRE_LENGTH} characters)"
        
        # Validate description
        if 'description' in data and data['description'] is not None:
            description = str(data['description']).strip()
            if len(description) > self.config.MAX_DESCRIPTION_LENGTH:
                return False, f"Description too long (max {self.config.MAX_DESCRIPTION_LENGTH} characters)"
        
        return True, ""
    
    def _generate_id(self) -> int:
        """Generate a new unique ID for a book"""
        if not self.books:
            return 1
        return max(book["id"] for book in self.books) + 1
    
    def get_all_books(self, page: int = 1, per_page: int = None) -> Dict[str, Any]:
        """Get all books with optional pagination"""
        if per_page is None:
            per_page = self.config.DEFAULT_PAGE_SIZE
        
        per_page = min(per_page, self.config.MAX_PAGE_SIZE)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_books = self.books[start_idx:end_idx]
        total_books = len(self.books)
        total_pages = (total_books + per_page - 1) // per_page
        
        return {
            "success": True,
            "data": paginated_books,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_books,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_book_by_id(self, book_id: int) -> Dict[str, Any]:
        """Get a specific book by ID"""
        book = next((book for book in self.books if book["id"] == book_id), None)
        
        if book is None:
            return {
                "success": False,
                "error": "Book not found",
                "book_id": book_id
            }
        
        return {
            "success": True,
            "data": book
        }
    
    def create_book(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new book"""
        # Validate data
        is_valid, error_msg = self._validate_book_data(data)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Create new book
        new_book = {
            "id": self._generate_id(),
            "title": str(data["title"]).strip(),
            "author": str(data["author"]).strip(),
            "year": data.get("year"),
            "genre": data.get("genre"),
            "description": data.get("description", ""),
            "created_at": datetime.now().isoformat()
        }
        
        self.books.append(new_book)
        
        # Save to file
        if self._save_books(self.books):
            return {
                "success": True,
                "data": new_book,
                "message": "Book created successfully"
            }
        else:
            # Remove from memory if save failed
            self.books.remove(new_book)
            return {
                "success": False,
                "error": "Failed to save book to storage"
            }
    
    def update_book(self, book_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing book"""
        book = next((book for book in self.books if book["id"] == book_id), None)
        
        if book is None:
            return {
                "success": False,
                "error": "Book not found",
                "book_id": book_id
            }
        
        # Validate data
        is_valid, error_msg = self._validate_book_data(data, is_update=True)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Update fields
        if "title" in data:
            book["title"] = str(data["title"]).strip()
        if "author" in data:
            book["author"] = str(data["author"]).strip()
        if "year" in data:
            book["year"] = data["year"] if data["year"] is not None else None
        if "genre" in data:
            book["genre"] = str(data["genre"]).strip() if data["genre"] else None
        if "description" in data:
            book["description"] = str(data["description"]).strip() if data["description"] else ""
        
        book["updated_at"] = datetime.now().isoformat()
        
        # Save to file
        if self._save_books(self.books):
            return {
                "success": True,
                "data": book,
                "message": "Book updated successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to save changes to storage"
            }
    
    def delete_book(self, book_id: int) -> Dict[str, Any]:
        """Delete a book"""
        book = next((book for book in self.books if book["id"] == book_id), None)
        
        if book is None:
            return {
                "success": False,
                "error": "Book not found",
                "book_id": book_id
            }
        
        self.books.remove(book)
        
        # Save to file
        if self._save_books(self.books):
            return {
                "success": True,
                "message": "Book deleted successfully",
                "deleted_book": book
            }
        else:
            # Restore book if save failed
            self.books.append(book)
            return {
                "success": False,
                "error": "Failed to delete book from storage"
            }
    
    def search_books(self, query: str, page: int = 1, per_page: int = None) -> Dict[str, Any]:
        """Search books by title, author, genre, or description"""
        if not query or not query.strip():
            return {
                "success": False,
                "error": "Search query is required"
            }
        
        query = query.strip()
        if len(query) < self.config.MIN_SEARCH_QUERY_LENGTH:
            return {
                "success": False,
                "error": f"Search query must be at least {self.config.MIN_SEARCH_QUERY_LENGTH} characters"
            }
        
        if len(query) > self.config.MAX_SEARCH_QUERY_LENGTH:
            return {
                "success": False,
                "error": f"Search query too long (max {self.config.MAX_SEARCH_QUERY_LENGTH} characters)"
            }
        
        query_lower = query.lower()
        results = []
        
        for book in self.books:
            # Search in title, author, genre, and description
            if (query_lower in book.get("title", "").lower() or
                query_lower in book.get("author", "").lower() or
                query_lower in book.get("genre", "").lower() or
                query_lower in book.get("description", "").lower()):
                results.append(book)
        
        # Apply pagination
        if per_page is None:
            per_page = self.config.DEFAULT_PAGE_SIZE
        
        per_page = min(per_page, self.config.MAX_PAGE_SIZE)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_results = results[start_idx:end_idx]
        total_results = len(results)
        total_pages = (total_results + per_page - 1) // per_page
        
        return {
            "success": True,
            "data": paginated_results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total_results,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            },
            "query": query
        }
    
    def get_books_by_author(self, author: str) -> List[Dict[str, Any]]:
        """Get all books by a specific author"""
        author_lower = author.lower()
        return [book for book in self.books if book.get("author", "").lower() == author_lower]
    
    def get_books_by_genre(self, genre: str) -> List[Dict[str, Any]]:
        """Get all books by a specific genre"""
        genre_lower = genre.lower()
        return [book for book in self.books if book.get("genre", "").lower() == genre_lower] 