"""
Authentication routes for the Book API.
Handles login, registration, token refresh, and user management.
"""

from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth import require_auth, require_admin, get_current_user_id
from config import Config

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize user model
user_model = User(Config())

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            return jsonify({
                "success": False,
                "error": "Missing required fields",
                "message": "Username and password are required"
            }), 400
        
        # Authenticate user
        result = user_model.authenticate_user(data['username'], data['password'])
        
        if not result:
            return jsonify({
                "success": False,
                "error": "Invalid credentials",
                "message": "Username or password is incorrect"
            }), 401
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "Login successful"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        result = user_model.create_user(data)
        
        status_code = 201 if result["success"] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token endpoint"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return jsonify({
                "success": False,
                "error": "Missing refresh token",
                "message": "refresh_token is required"
            }), 400
        
        # Refresh token
        result = user_model.refresh_token(refresh_token)
        
        if not result:
            return jsonify({
                "success": False,
                "error": "Invalid refresh token",
                "message": "Refresh token is invalid or expired"
            }), 401
        
        return jsonify({
            "success": True,
            "data": result,
            "message": "Token refreshed successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_current_user_id()
        result = user_model.get_user_by_id(current_user_id)
        
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update current user profile"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        current_user_id = get_current_user_id()
        data = request.get_json()
        
        # Remove role and is_active from data (users can't change their own role)
        data.pop('role', None)
        data.pop('is_active', None)
        
        result = user_model.update_user(current_user_id, data, current_user_id)
        
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

@auth_bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    """Get all users (admin only)"""
    try:
        result = user_model.get_all_users()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """Get a specific user (admin only)"""
    try:
        result = user_model.get_user_by_id(user_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id):
    """Update a user (admin only)"""
    try:
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        current_user_id = get_current_user_id()
        result = user_model.update_user(user_id, data, current_user_id)
        
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

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete a user (admin only)"""
    try:
        current_user_id = get_current_user_id()
        result = user_model.delete_user(user_id, current_user_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """User logout endpoint (client-side token removal)"""
    return jsonify({
        "success": True,
        "message": "Logout successful. Please remove the token from client storage."
    }) 