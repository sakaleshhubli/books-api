"""
Utils package for the Book API.
Contains utility functions and helper classes.
"""

from .data_manager import DataManager
from .auth import (
    require_auth, require_roles, require_admin, require_moderator_or_admin,
    optional_auth, get_current_user, get_current_user_id, get_current_user_role,
    is_authenticated, has_role, has_any_role, is_admin, is_moderator_or_admin,
    can_edit_resource, can_delete_resource
)

__all__ = [
    'DataManager',
    'require_auth', 'require_roles', 'require_admin', 'require_moderator_or_admin',
    'optional_auth', 'get_current_user', 'get_current_user_id', 'get_current_user_role',
    'is_authenticated', 'has_role', 'has_any_role', 'is_admin', 'is_moderator_or_admin',
    'can_edit_resource', 'can_delete_resource'
] 