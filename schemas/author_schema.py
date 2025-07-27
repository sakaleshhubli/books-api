"""
Author schema for data serialization and validation.
"""

from datetime import datetime
from typing import Dict, Any, Optional

class AuthorSchema:
    """Author data schema and serialization"""
    
    @staticmethod
    def serialize(author: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize an author object for API response"""
        return {
            "id": author.get("id"),
            "name": author.get("name"),
            "birth_year": author.get("birth_year"),
            "death_year": author.get("death_year"),
            "nationality": author.get("nationality"),
            "biography": author.get("biography", ""),
            "created_at": author.get("created_at"),
            "updated_at": author.get("updated_at")
        }
    
    @staticmethod
    def serialize_list(authors: list) -> list:
        """Serialize a list of authors"""
        return [AuthorSchema.serialize(author) for author in authors]
    
    @staticmethod
    def deserialize(data: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize and clean author data from request"""
        return {
            "name": data.get("name", "").strip() if data.get("name") else None,
            "birth_year": data.get("birth_year"),
            "death_year": data.get("death_year"),
            "nationality": data.get("nationality", "").strip() if data.get("nationality") else None,
            "biography": data.get("biography", "").strip() if data.get("biography") else ""
        }
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any]) -> tuple[bool, str]:
        """Validate required fields for author creation"""
        if not data.get("name"):
            return False, "Missing required field: name"
        return True, ""
    
    @staticmethod
    def get_author_summary(author: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of author information"""
        return {
            "id": author.get("id"),
            "name": author.get("name"),
            "birth_year": author.get("birth_year"),
            "death_year": author.get("death_year"),
            "nationality": author.get("nationality")
        } 