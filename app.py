"""
Main application file for the Book API.
This is the entry point for the Flask application.
"""

from flask import Flask, jsonify, request, render_template
from datetime import datetime
import os
from config import config
from routes import books_bp, authors_bp, auth_bp
from utils import DataManager

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(auth_bp)
    
    # Initialize data manager
    data_manager = DataManager(app.config)
    
    # Frontend routes
    @app.route('/', methods=['GET'])
    def index():
        """Serve the main frontend page"""
        return render_template('index.html')
    
    @app.route('/books', methods=['GET'])
    def books_page():
        """Serve the books page"""
        return render_template('index.html')
    
    @app.route('/authors', methods=['GET'])
    def authors_page():
        """Serve the authors page"""
        return render_template('index.html')
    
    @app.route('/login', methods=['GET'])
    def login_page():
        """Serve the login page"""
        return render_template('index.html')
    
    @app.route('/register', methods=['GET'])
    def register_page():
        """Serve the register page"""
        return render_template('index.html')
    
    @app.route('/profile', methods=['GET'])
    def profile_page():
        """Serve the profile page"""
        return render_template('index.html')
    
    # API documentation endpoint
    @app.route('/api', methods=['GET'])
    def api_docs():
        """API documentation endpoint"""
        return jsonify({
            "message": "Welcome to the Book API",
            "version": app.config['API_VERSION'],
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "health": {
                    "url": "/health",
                    "method": "GET",
                    "description": "Health check endpoint"
                },
                "books": {
                    "get_all": {
                        "url": "/api/books",
                        "method": "GET",
                        "description": "Get all books (with pagination)",
                        "query_params": ["page", "per_page"]
                    },
                    "get_by_id": {
                        "url": "/api/books/<id>",
                        "method": "GET",
                        "description": "Get a specific book by ID"
                    },
                    "create": {
                        "url": "/api/books",
                        "method": "POST",
                        "description": "Create a new book",
                        "required_fields": ["title", "author"]
                    },
                    "update": {
                        "url": "/api/books/<id>",
                        "method": "PUT",
                        "description": "Update an existing book"
                    },
                    "delete": {
                        "url": "/api/books/<id>",
                        "method": "DELETE",
                        "description": "Delete a book"
                    },
                    "search": {
                        "url": "/api/books/search?q=<query>",
                        "method": "GET",
                        "description": "Search books by title, author, genre, or description",
                        "query_params": ["q", "page", "per_page"]
                    },
                    "by_author": {
                        "url": "/api/books/by-author/<author_name>",
                        "method": "GET",
                        "description": "Get all books by a specific author"
                    },
                    "by_genre": {
                        "url": "/api/books/by-genre/<genre>",
                        "method": "GET",
                        "description": "Get all books by a specific genre"
                    }
                },
                "authors": {
                    "get_all": {
                        "url": "/api/authors",
                        "method": "GET",
                        "description": "Get all authors"
                    },
                    "get_by_id": {
                        "url": "/api/authors/<id>",
                        "method": "GET",
                        "description": "Get a specific author by ID"
                    },
                    "create": {
                        "url": "/api/authors",
                        "method": "POST",
                        "description": "Create a new author",
                        "required_fields": ["name"]
                    },
                    "update": {
                        "url": "/api/authors/<id>",
                        "method": "PUT",
                        "description": "Update an existing author"
                    },
                    "delete": {
                        "url": "/api/authors/<id>",
                        "method": "DELETE",
                        "description": "Delete an author"
                    }
                },
                "authentication": {
                    "login": {
                        "url": "/api/auth/login",
                        "method": "POST",
                        "description": "User login",
                        "required_fields": ["username", "password"]
                    },
                    "register": {
                        "url": "/api/auth/register",
                        "method": "POST",
                        "description": "User registration",
                        "required_fields": ["username", "email", "password"]
                    },
                    "refresh": {
                        "url": "/api/auth/refresh",
                        "method": "POST",
                        "description": "Refresh access token",
                        "required_fields": ["refresh_token"]
                    },
                    "profile": {
                        "url": "/api/auth/profile",
                        "method": "GET",
                        "description": "Get current user profile (authenticated)"
                    },
                    "update_profile": {
                        "url": "/api/auth/profile",
                        "method": "PUT",
                        "description": "Update current user profile (authenticated)"
                    },
                    "logout": {
                        "url": "/api/auth/logout",
                        "method": "POST",
                        "description": "User logout (authenticated)"
                    },
                    "get_users": {
                        "url": "/api/auth/users",
                        "method": "GET",
                        "description": "Get all users (admin only)"
                    },
                    "get_user": {
                        "url": "/api/auth/users/<id>",
                        "method": "GET",
                        "description": "Get specific user (admin only)"
                    },
                    "update_user": {
                        "url": "/api/auth/users/<id>",
                        "method": "PUT",
                        "description": "Update user (admin only)"
                    },
                    "delete_user": {
                        "url": "/api/auth/users/<id>",
                        "method": "DELETE",
                        "description": "Delete user (admin only)"
                    }
                },
                "data_management": {
                    "stats": {
                        "url": "/api/data/stats",
                        "method": "GET",
                        "description": "Get data statistics"
                    },
                    "backup": {
                        "url": "/api/data/backup",
                        "method": "POST",
                        "description": "Create a backup of current data",
                        "optional_body": {"backup_name": "custom_name"}
                    },
                    "reset": {
                        "url": "/api/data/reset",
                        "method": "POST",
                        "description": "Reset data to defaults"
                    },
                    "export": {
                        "url": "/api/data/export",
                        "method": "GET",
                        "description": "Export current data"
                    },
                    "import": {
                        "url": "/api/data/import",
                        "method": "POST",
                        "description": "Import data from file",
                        "body": {"import_file": "filename.json"}
                    }
                }
            },
            "features": [
                "Modular architecture with blueprints",
                "JWT-based authentication",
                "Role-based access control (RBAC)",
                "Persistent storage in JSON files",
                "Input validation and sanitization",
                "Comprehensive error handling",
                "Search functionality with pagination",
                "Data management (backup/restore/export/import)",
                "Health monitoring",
                "RESTful API design"
            ],
            "configuration": {
                "environment": config_name,
                "debug": app.config['DEBUG'],
                "max_title_length": app.config['MAX_TITLE_LENGTH'],
                "max_author_length": app.config['MAX_AUTHOR_LENGTH'],
                "max_genre_length": app.config['MAX_GENRE_LENGTH'],
                "default_page_size": app.config['DEFAULT_PAGE_SIZE']
            }
        })
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "message": "Book API is running successfully",
            "version": app.config['API_VERSION'],
            "environment": config_name
        })
    
    # Data management endpoints
    @app.route('/api/data/stats', methods=['GET'])
    def get_data_stats():
        """Get data statistics"""
        result = data_manager.get_data_stats()
        return jsonify(result)
    
    @app.route('/api/data/backup', methods=['POST'])
    def create_backup():
        """Create a backup of current data"""
        backup_name = request.json.get('backup_name') if request.is_json else None
        result = data_manager.backup_data(backup_name)
        return jsonify(result)
    
    @app.route('/api/data/reset', methods=['POST'])
    def reset_data():
        """Reset data to defaults"""
        result = data_manager.reset_to_defaults()
        return jsonify(result)
    
    @app.route('/api/data/export', methods=['GET'])
    def export_data():
        """Export current data"""
        result = data_manager.export_data()
        return jsonify(result)
    
    @app.route('/api/data/import', methods=['POST'])
    def import_data():
        """Import data from file"""
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        import_file = request.json.get('import_file')
        if not import_file:
            return jsonify({
                "success": False,
                "error": "import_file parameter is required"
            }), 400
        
        result = data_manager.import_data(import_file)
        return jsonify(result)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "timestamp": datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "Method not allowed",
            "message": "The HTTP method is not supported for this endpoint",
            "timestamp": datetime.now().isoformat()
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }), 500
    
    return app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    print("🚀 Starting Book API with Frontend...")
    print(f"📚 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🔧 Debug mode: {app.config['DEBUG']}")
    print("\n🌐 Frontend:")
    print("  - Home: http://localhost:5000/")
    print("  - Books: http://localhost:5000/books")
    print("  - Authors: http://localhost:5000/authors")
    print("  - Login: http://localhost:5000/login")
    print("  - Register: http://localhost:5000/register")
    print("  - Profile: http://localhost:5000/profile")
    print("\n📋 API Endpoints:")
    print("  - GET  /health")
    print("  - POST /api/auth/login")
    print("  - POST /api/auth/register")
    print("  - POST /api/auth/refresh")
    print("  - GET  /api/auth/profile")
    print("  - PUT  /api/auth/profile")
    print("  - POST /api/auth/logout")
    print("  - GET  /api/books")
    print("  - GET  /api/books/<id>")
    print("  - POST /api/books (moderator/admin)")
    print("  - PUT  /api/books/<id> (moderator/admin)")
    print("  - DELETE /api/books/<id> (moderator/admin)")
    print("  - GET  /api/books/search?q=<query>")
    print("  - GET  /api/books/by-author/<author>")
    print("  - GET  /api/books/by-genre/<genre>")
    print("  - GET  /api/authors")
    print("  - GET  /api/authors/<id>")
    print("  - POST /api/authors")
    print("  - PUT  /api/authors/<id>")
    print("  - DELETE /api/authors/<id>")
    print("  - GET  /api/data/stats")
    print("  - POST /api/data/backup")
    print("  - POST /api/data/reset")
    print("  - GET  /api/data/export")
    print("  - POST /api/data/import")
    print(f"\n🌐 Server starting on http://localhost:5000")
    print("📖 Frontend available at: http://localhost:5000/")
    print("🔗 API Documentation available at: http://localhost:5000/api")
    print("💚 Health check available at: http://localhost:5000/health")
    
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000) 