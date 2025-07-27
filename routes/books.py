"""
Book routes for the Book API.
Handles all book-related HTTP endpoints.
"""

from flask import Blueprint, request, jsonify
from models.book import Book
from utils.auth import require_auth, require_moderator_or_admin, optional_auth, get_current_user_id
from config import Config

# Create blueprint
books_bp = Blueprint('books', __name__, url_prefix='/api/books')

# Initialize book model
book_model = Book(Config())

@books_bp.route('/', methods=['GET'])
@optional_auth
def get_books():
    """Get all books with optional pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', None, type=int)
        
        if page < 1:
            return jsonify({
                "success": False,
                "error": "Page number must be greater than 0"
            }), 400
        
        result = book_model.get_all_books(page=page, per_page=per_page)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
@optional_auth
def get_book(book_id):
    """Get a specific book by ID"""
    try:
        result = book_model.get_book_by_id(book_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/', methods=['POST'])
@require_moderator_or_admin
def create_book():
    """Create a new book (moderator/admin only)"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        result = book_model.create_book(data)
        status_code = 201 if result["success"] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
@require_moderator_or_admin
def update_book(book_id):
    """Update an existing book (moderator/admin only)"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        result = book_model.update_book(book_id, data)
        
        if result["success"]:
            status_code = 200
        elif "not found" in result.get("error", "").lower():
            status_code = 404
        else:
            status_code = 400
        
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
@require_moderator_or_admin
def delete_book(book_id):
    """Delete a book (moderator/admin only)"""
    try:
        result = book_model.delete_book(book_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/search', methods=['GET'])
@optional_auth
def search_books():
    """Search books by title, author, genre, or description"""
    try:
        query = request.args.get('q', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', None, type=int)
        
        if page < 1:
            return jsonify({
                "success": False,
                "error": "Page number must be greater than 0"
            }), 400
        
        result = book_model.search_books(query, page=page, per_page=per_page)
        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/by-author/<author_name>', methods=['GET'])
@optional_auth
def get_books_by_author(author_name):
    """Get all books by a specific author"""
    try:
        books = book_model.get_books_by_author(author_name)
        return jsonify({
            "success": True,
            "data": books,
            "count": len(books),
            "author": author_name
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@books_bp.route('/by-genre/<genre>', methods=['GET'])
@optional_auth
def get_books_by_genre(genre):
    """Get all books by a specific genre"""
    try:
        books = book_model.get_books_by_genre(genre)
        return jsonify({
            "success": True,
            "data": books,
            "count": len(books),
            "genre": genre
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500 