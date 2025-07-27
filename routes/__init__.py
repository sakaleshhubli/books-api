"""
Routes package for the Book API.
Contains all API route handlers.
"""

from .books import books_bp
from .authors import authors_bp
from .auth import auth_bp

__all__ = ['books_bp', 'authors_bp', 'auth_bp'] 