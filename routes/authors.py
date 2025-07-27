"""
Author routes for the Book API.
Handles all author-related HTTP endpoints.
"""

from flask import Blueprint, request, jsonify
from models.author import Author
from config import Config

# Create blueprint
authors_bp = Blueprint('authors', __name__, url_prefix='/api/authors')

# Initialize author model
author_model = Author(Config())

@authors_bp.route('/', methods=['GET'])
def get_authors():
    """Get all authors"""
    try:
        result = author_model.get_all_authors()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@authors_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """Get a specific author by ID"""
    try:
        result = author_model.get_author_by_id(author_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@authors_bp.route('/', methods=['POST'])
def create_author():
    """Create a new author"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        result = author_model.create_author(data)
        status_code = 201 if result["success"] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@authors_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """Update an existing author"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        result = author_model.update_author(author_id, data)
        
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

@authors_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    """Delete an author"""
    try:
        result = author_model.delete_author(author_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500 