"""
Authentication utilities and decorators for the Book API.
Provides JWT token validation and role-based access control.
"""

from functools import wraps
from flask import request, jsonify, g
from typing import List, Optional, Callable
from models.user import User
from config import Config

def get_token_from_header() -> Optional[str]:
    """Extract JWT token from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]

def require_auth(f: Callable) -> Callable:
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if not token:
            return jsonify({
                "success": False,
                "error": "Authentication required",
                "message": "Missing or invalid Authorization header"
            }), 401
        
        user_model = User(Config())
        payload = user_model.verify_token(token)
        
        if not payload:
            return jsonify({
                "success": False,
                "error": "Invalid token",
                "message": "Token is invalid or expired"
            }), 401
        
        # Store user info in Flask's g object
        g.current_user = payload
        return f(*args, **kwargs)
    
    return decorated_function

def require_roles(roles: List[str]) -> Callable:
    """Decorator to require specific roles"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # First check authentication
            token = get_token_from_header()
            if not token:
                return jsonify({
                    "success": False,
                    "error": "Authentication required",
                    "message": "Missing or invalid Authorization header"
                }), 401
            
            user_model = User(Config())
            payload = user_model.verify_token(token)
            
            if not payload:
                return jsonify({
                    "success": False,
                    "error": "Invalid token",
                    "message": "Token is invalid or expired"
                }), 401
            
            # Check role permissions
            user_role = payload.get('role', 'user')
            if user_role not in roles:
                return jsonify({
                    "success": False,
                    "error": "Insufficient permissions",
                    "message": f"Required roles: {', '.join(roles)}. Your role: {user_role}"
                }), 403
            
            # Store user info in Flask's g object
            g.current_user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def require_admin(f: Callable) -> Callable:
    """Decorator to require admin role"""
    return require_roles(['admin'])(f)

def require_moderator_or_admin(f: Callable) -> Callable:
    """Decorator to require moderator or admin role"""
    return require_roles(['moderator', 'admin'])(f)

def optional_auth(f: Callable) -> Callable:
    """Decorator for optional authentication (public endpoints with enhanced features for authenticated users)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = get_token_from_header()
        if token:
            user_model = User(Config())
            payload = user_model.verify_token(token)
            if payload:
                g.current_user = payload
            else:
                g.current_user = None
        else:
            g.current_user = None
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user() -> Optional[dict]:
    """Get current authenticated user from Flask's g object"""
    return getattr(g, 'current_user', None)

def get_current_user_id() -> Optional[int]:
    """Get current user ID"""
    user = get_current_user()
    return user.get('user_id') if user else None

def get_current_user_role() -> Optional[str]:
    """Get current user role"""
    user = get_current_user()
    return user.get('role', 'user') if user else None

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return get_current_user() is not None

def has_role(role: str) -> bool:
    """Check if current user has specific role"""
    user = get_current_user()
    return user and user.get('role') == role

def has_any_role(roles: List[str]) -> bool:
    """Check if current user has any of the specified roles"""
    user = get_current_user()
    return user and user.get('role') in roles

def is_admin() -> bool:
    """Check if current user is admin"""
    return has_role('admin')

def is_moderator_or_admin() -> bool:
    """Check if current user is moderator or admin"""
    return has_any_role(['moderator', 'admin'])

def can_edit_resource(resource_user_id: int) -> bool:
    """Check if current user can edit a resource (owner or admin)"""
    current_user = get_current_user()
    if not current_user:
        return False
    
    # Admin can edit any resource
    if current_user.get('role') == 'admin':
        return True
    
    # Users can edit their own resources
    return current_user.get('user_id') == resource_user_id

def can_delete_resource(resource_user_id: int) -> bool:
    """Check if current user can delete a resource (owner or admin)"""
    current_user = get_current_user()
    if not current_user:
        return False
    
    # Admin can delete any resource
    if current_user.get('role') == 'admin':
        return True
    
    # Users can delete their own resources
    return current_user.get('user_id') == resource_user_id 