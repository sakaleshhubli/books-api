"""
Author model and data operations.
Handles all author-related data operations.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from config import Config

class Author:
    """Author model and data operations"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.authors = self._load_authors()
    
    def _load_authors(self) -> List[Dict[str, Any]]:
        """Load authors from JSON file"""
        if os.path.exists(self.config.AUTHORS_FILE):
            try:
                with open(self.config.AUTHORS_FILE, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        return data
                    else:
                        print("Invalid JSON structure, using default authors")
                        return self._get_default_authors()
            except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
                print(f"Error loading authors: {e}")
                return self._get_default_authors()
        else:
            # Create file with default authors
            default_authors = self._get_default_authors()
            self._save_authors(default_authors)
            return default_authors
    
    def _save_authors(self, authors_data: List[Dict[str, Any]]) -> bool:
        """Save authors to JSON file"""
        try:
            with open(self.config.AUTHORS_FILE, 'w', encoding='utf-8') as file:
                json.dump(authors_data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving authors to file: {e}")
            return False
    
    def _get_default_authors(self) -> List[Dict[str, Any]]:
        """Load default authors from external JSON file"""
        try:
            if os.path.exists(self.config.DEFAULT_AUTHORS_FILE):
                with open(self.config.DEFAULT_AUTHORS_FILE, 'r', encoding='utf-8') as file:
                    default_authors = json.load(file)
                    if isinstance(default_authors, list):
                        return default_authors
                    else:
                        print("Invalid default authors JSON structure")
                        return self._get_fallback_authors()
            else:
                print(f"Default authors file not found: {self.config.DEFAULT_AUTHORS_FILE}")
                return self._get_fallback_authors()
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading default authors: {e}")
            return self._get_fallback_authors()
    
    def _get_fallback_authors(self) -> List[Dict[str, Any]]:
        """Return minimal fallback authors if default file fails"""
        return [
            {
                "id": 1,
                "name": "Sample Author",
                "birth_year": 1990,
                "death_year": None,
                "nationality": "Unknown",
                "biography": "A sample author for testing purposes."
            }
        ]
    
    def _validate_author_data(self, data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, str]:
        """Validate author data"""
        if not isinstance(data, dict):
            return False, "Invalid data format"
        
        # Required fields for creation
        if not is_update:
            if 'name' not in data or not data['name']:
                return False, "Missing required field: name"
        
        # Validate name
        if 'name' in data:
            name = str(data['name']).strip()
            if not name:
                return False, "Name cannot be empty"
            if len(name) > self.config.MAX_AUTHOR_LENGTH:
                return False, f"Name too long (max {self.config.MAX_AUTHOR_LENGTH} characters)"
        
        # Validate birth year
        if 'birth_year' in data and data['birth_year'] is not None:
            try:
                birth_year = int(data['birth_year'])
                if birth_year < 1000 or birth_year > datetime.now().year:
                    return False, "Birth year must be between 1000 and current year"
            except (ValueError, TypeError):
                return False, "Birth year must be a valid integer"
        
        # Validate death year
        if 'death_year' in data and data['death_year'] is not None:
            try:
                death_year = int(data['death_year'])
                if death_year < 1000 or death_year > datetime.now().year:
                    return False, "Death year must be between 1000 and current year"
            except (ValueError, TypeError):
                return False, "Death year must be a valid integer"
        
        # Validate birth and death year relationship
        if ('birth_year' in data and data['birth_year'] is not None and 
            'death_year' in data and data['death_year'] is not None):
            if data['birth_year'] >= data['death_year']:
                return False, "Death year must be after birth year"
        
        return True, ""
    
    def _generate_id(self) -> int:
        """Generate a new unique ID for an author"""
        if not self.authors:
            return 1
        return max(author["id"] for author in self.authors) + 1
    
    def get_all_authors(self) -> Dict[str, Any]:
        """Get all authors"""
        return {
            "success": True,
            "data": self.authors,
            "count": len(self.authors),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_author_by_id(self, author_id: int) -> Dict[str, Any]:
        """Get a specific author by ID"""
        author = next((author for author in self.authors if author["id"] == author_id), None)
        
        if author is None:
            return {
                "success": False,
                "error": "Author not found",
                "author_id": author_id
            }
        
        return {
            "success": True,
            "data": author
        }
    
    def create_author(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new author"""
        # Validate data
        is_valid, error_msg = self._validate_author_data(data)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Create new author
        new_author = {
            "id": self._generate_id(),
            "name": str(data["name"]).strip(),
            "birth_year": data.get("birth_year"),
            "death_year": data.get("death_year"),
            "nationality": data.get("nationality"),
            "biography": data.get("biography", ""),
            "created_at": datetime.now().isoformat()
        }
        
        self.authors.append(new_author)
        
        # Save to file
        if self._save_authors(self.authors):
            return {
                "success": True,
                "data": new_author,
                "message": "Author created successfully"
            }
        else:
            # Remove from memory if save failed
            self.authors.remove(new_author)
            return {
                "success": False,
                "error": "Failed to save author to storage"
            }
    
    def update_author(self, author_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing author"""
        author = next((author for author in self.authors if author["id"] == author_id), None)
        
        if author is None:
            return {
                "success": False,
                "error": "Author not found",
                "author_id": author_id
            }
        
        # Validate data
        is_valid, error_msg = self._validate_author_data(data, is_update=True)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Update fields
        if "name" in data:
            author["name"] = str(data["name"]).strip()
        if "birth_year" in data:
            author["birth_year"] = data["birth_year"] if data["birth_year"] is not None else None
        if "death_year" in data:
            author["death_year"] = data["death_year"] if data["death_year"] is not None else None
        if "nationality" in data:
            author["nationality"] = str(data["nationality"]).strip() if data["nationality"] else None
        if "biography" in data:
            author["biography"] = str(data["biography"]).strip() if data["biography"] else ""
        
        author["updated_at"] = datetime.now().isoformat()
        
        # Save to file
        if self._save_authors(self.authors):
            return {
                "success": True,
                "data": author,
                "message": "Author updated successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to save changes to storage"
            }
    
    def delete_author(self, author_id: int) -> Dict[str, Any]:
        """Delete an author"""
        author = next((author for author in self.authors if author["id"] == author_id), None)
        
        if author is None:
            return {
                "success": False,
                "error": "Author not found",
                "author_id": author_id
            }
        
        self.authors.remove(author)
        
        # Save to file
        if self._save_authors(self.authors):
            return {
                "success": True,
                "message": "Author deleted successfully",
                "deleted_author": author
            }
        else:
            # Restore author if save failed
            self.authors.append(author)
            return {
                "success": False,
                "error": "Failed to delete author from storage"
            } 