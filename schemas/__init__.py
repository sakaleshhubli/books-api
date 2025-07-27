"""
Schemas package for the Book API.
Contains data serialization and validation schemas.
"""

from .book_schema import BookSchema
from .author_schema import AuthorSchema

__all__ = ['BookSchema', 'AuthorSchema'] 