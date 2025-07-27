"""
User model and authentication operations.
Handles user management, authentication, and JWT token operations.
"""

import json
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from config import Config

class User:
    """User model and authentication operations"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.users = self._load_users()
    
    def _load_users(self) -> List[Dict[str, Any]]:
        """Load users from JSON file"""
        if os.path.exists(self.config.USERS_FILE):
            try:
                with open(self.config.USERS_FILE, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        return data
                    else:
                        print("Invalid JSON structure, using default users")
                        return self._get_default_users()
            except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
                print(f"Error loading users: {e}")
                return self._get_default_users()
        else:
            # Create file with default users
            default_users = self._get_default_users()
            self._save_users(default_users)
            return default_users
    
    def _save_users(self, users_data: List[Dict[str, Any]]) -> bool:
        """Save users to JSON file"""
        try:
            with open(self.config.USERS_FILE, 'w', encoding='utf-8') as file:
                json.dump(users_data, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving users to file: {e}")
            return False
    
    def _get_default_users(self) -> List[Dict[str, Any]]:
        """Load default users from external JSON file"""
        try:
            if os.path.exists(self.config.DEFAULT_USERS_FILE):
                with open(self.config.DEFAULT_USERS_FILE, 'r', encoding='utf-8') as file:
                    default_users = json.load(file)
                    if isinstance(default_users, list):
                        return default_users
                    else:
                        print("Invalid default users JSON structure")
                        return self._get_fallback_users()
            else:
                print(f"Default users file not found: {self.config.DEFAULT_USERS_FILE}")
                return self._get_fallback_users()
        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Error loading default users: {e}")
            return self._get_fallback_users()
    
    def _get_fallback_users(self) -> List[Dict[str, Any]]:
        """Return minimal fallback users if default file fails"""
        # Create admin user with hashed password
        admin_password = self._hash_password("admin123")
        return [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@example.com",
                "password_hash": admin_password,
                "role": "admin",
                "is_active": True,
                "created_at": datetime.now().isoformat()
            }
        ]
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def _validate_user_data(self, data: Dict[str, Any], is_update: bool = False) -> Tuple[bool, str]:
        """Validate user data"""
        if not isinstance(data, dict):
            return False, "Invalid data format"
        
        # Required fields for creation
        if not is_update:
            required_fields = ['username', 'email', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return False, f"Missing required field: {field}"
        
        # Validate username
        if 'username' in data:
            username = str(data['username']).strip()
            if not username:
                return False, "Username cannot be empty"
            if len(username) < self.config.MIN_USERNAME_LENGTH:
                return False, f"Username too short (min {self.config.MIN_USERNAME_LENGTH} characters)"
            if len(username) > self.config.MAX_USERNAME_LENGTH:
                return False, f"Username too long (max {self.config.MAX_USERNAME_LENGTH} characters)"
            
            # Check for duplicate username
            if not is_update:
                if any(user['username'] == username for user in self.users):
                    return False, "Username already exists"
        
        # Validate email
        if 'email' in data:
            email = str(data['email']).strip().lower()
            if not email:
                return False, "Email cannot be empty"
            if len(email) > self.config.MAX_EMAIL_LENGTH:
                return False, f"Email too long (max {self.config.MAX_EMAIL_LENGTH} characters)"
            if '@' not in email or '.' not in email:
                return False, "Invalid email format"
            
            # Check for duplicate email
            if not is_update:
                if any(user['email'] == email for user in self.users):
                    return False, "Email already exists"
        
        # Validate password
        if 'password' in data:
            password = str(data['password'])
            if len(password) < self.config.MIN_PASSWORD_LENGTH:
                return False, f"Password too short (min {self.config.MIN_PASSWORD_LENGTH} characters)"
            if len(password) > self.config.MAX_PASSWORD_LENGTH:
                return False, f"Password too long (max {self.config.MAX_PASSWORD_LENGTH} characters)"
        
        # Validate role
        if 'role' in data:
            valid_roles = ['user', 'moderator', 'admin']
            if data['role'] not in valid_roles:
                return False, f"Invalid role. Must be one of: {', '.join(valid_roles)}"
        
        return True, ""
    
    def _generate_id(self) -> int:
        """Generate a new unique ID for a user"""
        if not self.users:
            return 1
        return max(user["id"] for user in self.users) + 1
    
    def _generate_tokens(self, user_id: int, username: str, role: str) -> Dict[str, str]:
        """Generate JWT access and refresh tokens"""
        # Access token payload
        access_payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'type': 'access',
            'exp': datetime.utcnow() + self.config.JWT_ACCESS_TOKEN_EXPIRES,
            'iat': datetime.utcnow()
        }
        
        # Refresh token payload
        refresh_payload = {
            'user_id': user_id,
            'username': username,
            'type': 'refresh',
            'exp': datetime.utcnow() + self.config.JWT_REFRESH_TOKEN_EXPIRES,
            'iat': datetime.utcnow()
        }
        
        # Generate tokens
        access_token = jwt.encode(access_payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer',
            'expires_in': int(self.config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
        }
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.config.JWT_SECRET_KEY, algorithms=[self.config.JWT_ALGORITHM])
            
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return None
            
            # Get user from database
            user = next((user for user in self.users if user['id'] == payload['user_id']), None)
            if not user or not user.get('is_active', True):
                return None
            
            return {
                'user_id': payload['user_id'],
                'username': payload['username'],
                'role': payload.get('role', 'user'),
                'type': payload['type']
            }
        except jwt.InvalidTokenError:
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password"""
        user = next((user for user in self.users if user['username'] == username), None)
        
        if not user or not user.get('is_active', True):
            return None
        
        if not self._verify_password(password, user['password_hash']):
            return None
        
        # Generate tokens
        tokens = self._generate_tokens(user['id'], user['username'], user['role'])
        
        return {
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'is_active': user.get('is_active', True)
            },
            'tokens': tokens
        }
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh an access token using a refresh token"""
        payload = self.verify_token(refresh_token)
        
        if not payload or payload['type'] != 'refresh':
            return None
        
        # Get user from database
        user = next((user for user in self.users if user['id'] == payload['user_id']), None)
        if not user or not user.get('is_active', True):
            return None
        
        # Generate new access token
        access_payload = {
            'user_id': user['id'],
            'username': user['username'],
            'role': user['role'],
            'type': 'access',
            'exp': datetime.utcnow() + self.config.JWT_ACCESS_TOKEN_EXPIRES,
            'iat': datetime.utcnow()
        }
        
        access_token = jwt.encode(access_payload, self.config.JWT_SECRET_KEY, algorithm=self.config.JWT_ALGORITHM)
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': int(self.config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())
        }
    
    def create_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        # Validate data
        is_valid, error_msg = self._validate_user_data(data)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Hash password
        password_hash = self._hash_password(data['password'])
        
        # Create new user
        new_user = {
            "id": self._generate_id(),
            "username": str(data['username']).strip(),
            "email": str(data['email']).strip().lower(),
            "password_hash": password_hash,
            "role": data.get('role', 'user'),
            "is_active": data.get('is_active', True),
            "created_at": datetime.now().isoformat()
        }
        
        self.users.append(new_user)
        
        # Save to file
        if self._save_users(self.users):
            return {
                "success": True,
                "data": {
                    'id': new_user['id'],
                    'username': new_user['username'],
                    'email': new_user['email'],
                    'role': new_user['role'],
                    'is_active': new_user['is_active']
                },
                "message": "User created successfully"
            }
        else:
            # Remove from memory if save failed
            self.users.remove(new_user)
            return {
                "success": False,
                "error": "Failed to save user to storage"
            }
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID"""
        user = next((user for user in self.users if user["id"] == user_id), None)
        
        if user is None:
            return {
                "success": False,
                "error": "User not found",
                "user_id": user_id
            }
        
        return {
            "success": True,
            "data": {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'is_active': user.get('is_active', True),
                'created_at': user.get('created_at')
            }
        }
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users (without sensitive data)"""
        users_data = []
        for user in self.users:
            users_data.append({
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'role': user['role'],
                'is_active': user.get('is_active', True),
                'created_at': user.get('created_at')
            })
        
        return {
            "success": True,
            "data": users_data,
            "count": len(users_data)
        }
    
    def update_user(self, user_id: int, data: Dict[str, Any], current_user_id: int) -> Dict[str, Any]:
        """Update an existing user"""
        user = next((user for user in self.users if user["id"] == user_id), None)
        
        if user is None:
            return {
                "success": False,
                "error": "User not found",
                "user_id": user_id
            }
        
        # Check permissions (users can only update their own profile, admins can update anyone)
        current_user = next((u for u in self.users if u["id"] == current_user_id), None)
        if not current_user or (current_user['role'] != 'admin' and current_user_id != user_id):
            return {
                "success": False,
                "error": "Insufficient permissions"
            }
        
        # Validate data
        is_valid, error_msg = self._validate_user_data(data, is_update=True)
        if not is_valid:
            return {
                "success": False,
                "error": error_msg
            }
        
        # Update fields
        if "username" in data:
            user["username"] = str(data["username"]).strip()
        if "email" in data:
            user["email"] = str(data["email"]).strip().lower()
        if "password" in data:
            user["password_hash"] = self._hash_password(data["password"])
        if "role" in data and current_user['role'] == 'admin':
            user["role"] = data["role"]
        if "is_active" in data and current_user['role'] == 'admin':
            user["is_active"] = data["is_active"]
        
        # Save to file
        if self._save_users(self.users):
            return {
                "success": True,
                "data": {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'is_active': user.get('is_active', True)
                },
                "message": "User updated successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to save changes to storage"
            }
    
    def delete_user(self, user_id: int, current_user_id: int) -> Dict[str, Any]:
        """Delete a user"""
        user = next((user for user in self.users if user["id"] == user_id), None)
        
        if user is None:
            return {
                "success": False,
                "error": "User not found",
                "user_id": user_id
            }
        
        # Check permissions (users can only delete their own account, admins can delete anyone)
        current_user = next((u for u in self.users if u["id"] == current_user_id), None)
        if not current_user or (current_user['role'] != 'admin' and current_user_id != user_id):
            return {
                "success": False,
                "error": "Insufficient permissions"
            }
        
        # Prevent deleting the last admin
        if user['role'] == 'admin':
            admin_count = sum(1 for u in self.users if u['role'] == 'admin' and u.get('is_active', True))
            if admin_count <= 1:
                return {
                    "success": False,
                    "error": "Cannot delete the last admin user"
                }
        
        self.users.remove(user)
        
        # Save to file
        if self._save_users(self.users):
            return {
                "success": True,
                "message": "User deleted successfully",
                "deleted_user": {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email']
                }
            }
        else:
            # Restore user if save failed
            self.users.append(user)
            return {
                "success": False,
                "error": "Failed to delete user from storage"
            } 