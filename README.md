# 📚 Book API

A comprehensive RESTful API for managing books and authors, built with Flask using a modular architecture. Perfect for learning REST APIs, testing with Postman, and building scalable applications.

## 🏗️ Project Structure

```
book_api/
│
├── app.py                      # Main application file
├── config.py                   # Configuration settings
├── books.json                  # Runtime book data (auto-generated)
├── authors.json                # Runtime author data (auto-generated)
├── .gitignore                  # Git ignore rules
│
├── data/                       # Default data files
│   ├── default_books.json      # Sample books (version controlled)
│   └── default_authors.json    # Sample authors (version controlled)
│
├── models/                     # Data layer
│   ├── __init__.py             # Initialize models
│   ├── book.py                 # Book model & operations
│   └── author.py               # Author model & operations
│
├── routes/                     # API endpoints
│   ├── __init__.py             # Initialize routes
│   ├── books.py                # Book routes (blueprint)
│   └── authors.py              # Author routes (blueprint)
│
├── schemas/                    # Data serialization
│   ├── __init__.py             # Initialize schemas
│   ├── book_schema.py          # Book serialization
│   └── author_schema.py        # Author serialization
│
├── utils/                      # Utilities
│   ├── __init__.py             # Initialize utils
│   └── data_manager.py         # Data management utilities
│
├── static/                     # Static files
├── templates/                  # HTML templates
├── requirements.txt            # Project dependencies
│
└── tests/                      # Test suite
    ├── __init__.py
    ├── test_models.py          # Model tests
    └── test_routes.py          # Route tests
```

## 🚀 Features

- **🌐 Modern Frontend**: Beautiful, responsive web interface with real-time interactions
- **🔐 JWT Authentication**: Secure token-based authentication system
- **👥 Role-Based Access Control (RBAC)**: User, moderator, and admin roles with different permissions
- **🏗️ Modular Architecture**: Clean separation of concerns with blueprints
- **💾 Persistent Storage**: JSON file-based data storage with automatic backups
- **✅ Comprehensive Validation**: Input validation and sanitization
- **🔍 Advanced Search**: Full-text search across multiple fields with pagination
- **📊 Data Management**: Backup, restore, export, import functionality
- **🔄 Pagination**: Built-in pagination for large datasets
- **🛡️ Error Handling**: Comprehensive error handling and logging
- **🎯 RESTful Design**: Follows REST API best practices
- **🧪 Testing**: Unit tests for models and routes
- **⚙️ Configuration Management**: Environment-based configuration
- **📝 Self-Documenting**: Comprehensive API documentation at root endpoint

## 🌐 Frontend Pages

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Dashboard with stats and quick actions |
| Books | `/books` | Browse and manage books |
| Authors | `/authors` | View and manage authors |
| Login | `/login` | User authentication |
| Register | `/register` | User registration |
| Profile | `/profile` | User profile management |

## 📋 API Endpoints

### 📖 Books

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/books` | Get all books (with pagination) | No |
| GET | `/api/books/<id>` | Get a specific book | No |
| POST | `/api/books` | Create a new book | Moderator/Admin |
| PUT | `/api/books/<id>` | Update an existing book | Moderator/Admin |
| DELETE | `/api/books/<id>` | Delete a book | Moderator/Admin |
| GET | `/api/books/search?q=<query>` | Search books | No |
| GET | `/api/books/by-author/<author>` | Get books by author | No |
| GET | `/api/books/by-genre/<genre>` | Get books by genre | No |

### 👨‍💼 Authors

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/authors` | Get all authors |
| GET | `/api/authors/<id>` | Get a specific author |
| POST | `/api/authors` | Create a new author |
| PUT | `/api/authors/<id>` | Update an existing author |
| DELETE | `/api/authors/<id>` | Delete an author |

### 🔐 Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/register` | User registration | No |
| POST | `/api/auth/refresh` | Refresh access token | No |
| GET | `/api/auth/profile` | Get current user profile | Yes |
| PUT | `/api/auth/profile` | Update current user profile | Yes |
| POST | `/api/auth/logout` | User logout | Yes |
| GET | `/api/auth/users` | Get all users | Admin only |
| GET | `/api/auth/users/<id>` | Get specific user | Admin only |
| PUT | `/api/auth/users/<id>` | Update user | Admin only |
| DELETE | `/api/auth/users/<id>` | Delete user | Admin only |

### 🛠️ Data Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/data/stats` | Get data statistics |
| POST | `/api/data/backup` | Create backup of current data |
| POST | `/api/data/reset` | Reset data to defaults |
| GET | `/api/data/export` | Export all data |
| POST | `/api/data/import` | Import data from file |

### 📋 General

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation |
| GET | `/health` | Health check |

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd book_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 👥 Default Users & Roles

The API comes with pre-configured users for testing:

| Username | Password | Role | Permissions |
|----------|----------|------|-------------|
| `admin` | `admin123` | Admin | Full access to all endpoints |
| `moderator` | `moderator123` | Moderator | Can manage books and authors |
| `user` | `user123` | User | Read-only access to books and authors |

### 🔐 Role Permissions

- **Admin**: Full access to all endpoints including user management
- **Moderator**: Can create, update, and delete books and authors
- **User**: Can only read books and authors (public endpoints)

## 🌐 Frontend Usage

### 🚀 Quick Start

1. **Start the application**: `python app.py`
2. **Open your browser**: Navigate to `http://localhost:5000`
3. **Login with demo credentials**:
   - **Admin**: `admin` / `admin123`
   - **Moderator**: `moderator` / `moderator123`
   - **User**: `user` / `user123`

### 🎨 Frontend Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Search**: Instant search across books and authors
- **Interactive Modals**: Add, edit, and delete books/authors with beautiful modals
- **Role-based UI**: Different features based on user permissions
- **Modern Animations**: Smooth transitions and hover effects
- **Dark/Light Theme**: Clean, modern interface

## 📮 Postman Setup

### 🚀 Quick Start

1. **Download Postman**: [postman.com](https://www.postman.com/downloads/)
2. **Import Collection**: Use the endpoints below to test the API
3. **Set Base URL**: `http://localhost:5000`

### 📋 Environment Variables

Create a Postman environment with these variables:

| Variable | Value |
|----------|-------|
| `base_url` | `http://localhost:5000` |
| `access_token` | (leave empty, will be set after login) |
| `book_id` | (leave empty, will be set dynamically) |
| `author_id` | (leave empty, will be set dynamically) |

## 📖 Usage Examples with Postman

### 🔐 Authentication Operations

#### 1. User Login
- **Method**: `POST`
- **URL**: `{{base_url}}/api/auth/login`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- **Response**: Returns access and refresh tokens
- **Save Token**: Copy the `access_token` from response for other requests

#### 2. User Registration
- **Method**: `POST`
- **URL**: `{{base_url}}/api/auth/register`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
  }
  ```

#### 3. Get User Profile (Authenticated)
- **Method**: `GET`
- **URL**: `{{base_url}}/api/auth/profile`
- **Headers**: 
  - `Authorization: Bearer {{access_token}}`

#### 4. Update User Profile (Authenticated)
- **Method**: `PUT`
- **URL**: `{{base_url}}/api/auth/profile`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body** (raw JSON):
  ```json
  {
    "email": "updated@example.com"
  }
  ```

#### 5. Refresh Access Token
- **Method**: `POST`
- **URL**: `{{base_url}}/api/auth/refresh`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "refresh_token": "your_refresh_token_here"
  }
  ```

#### 6. User Logout (Authenticated)
- **Method**: `POST`
- **URL**: `{{base_url}}/api/auth/logout`
- **Headers**: 
  - `Authorization: Bearer {{access_token}}`

### 📚 Books Operations

#### 1. Get All Books
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books`
- **Headers**: None required

#### 2. Get Books with Pagination
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books?page=1&per_page=5`
- **Headers**: None required

#### 3. Create a New Book (Requires Authentication)
- **Method**: `POST`
- **URL**: `{{base_url}}/api/books`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body** (raw JSON):
  ```json
  {
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937,
    "genre": "Fantasy",
    "description": "A fantasy novel about a hobbit's journey to help reclaim a dwarf kingdom."
  }
  ```

#### 4. Get a Specific Book
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books/1`
- **Headers**: None required

#### 5. Update a Book (Requires Authentication)
- **Method**: `PUT`
- **URL**: `{{base_url}}/api/books/1`
- **Headers**: 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body** (raw JSON):
  ```json
  {
    "title": "The Hobbit (Updated)",
    "year": 1938,
    "description": "Updated description of the hobbit's journey."
  }
  ```

#### 6. Search Books
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books/search?q=fantasy`
- **Headers**: None required

#### 7. Get Books by Author
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books/by-author/J.R.R. Tolkien`
- **Headers**: None required

#### 8. Get Books by Genre
- **Method**: `GET`
- **URL**: `{{base_url}}/api/books/by-genre/Fantasy`
- **Headers**: None required

#### 9. Delete a Book (Requires Authentication)
- **Method**: `DELETE`
- **URL**: `{{base_url}}/api/books/1`
- **Headers**: 
  - `Authorization: Bearer {{access_token}}`

### 👨‍💼 Authors Operations

#### 1. Get All Authors
- **Method**: `GET`
- **URL**: `{{base_url}}/api/authors`
- **Headers**: None required

#### 2. Create a New Author
- **Method**: `POST`
- **URL**: `{{base_url}}/api/authors`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "name": "J.R.R. Tolkien",
    "birth_year": 1892,
    "death_year": 1973,
    "nationality": "British",
    "biography": "English writer, poet, philologist, and university professor."
  }
  ```

#### 3. Get a Specific Author
- **Method**: `GET`
- **URL**: `{{base_url}}/api/authors/1`
- **Headers**: None required

#### 4. Update an Author
- **Method**: `PUT`
- **URL**: `{{base_url}}/api/authors/1`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "biography": "Updated biography of J.R.R. Tolkien."
  }
  ```

#### 5. Delete an Author
- **Method**: `DELETE`
- **URL**: `{{base_url}}/api/authors/1`
- **Headers**: None required

### 🛠️ Data Management Operations

#### 1. Get Data Statistics
- **Method**: `GET`
- **URL**: `{{base_url}}/api/data/stats`
- **Headers**: None required

#### 2. Create Backup
- **Method**: `POST`
- **URL**: `{{base_url}}/api/data/backup`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON, optional):
  ```json
  {
    "backup_name": "my_backup"
  }
  ```

#### 3. Reset to Defaults
- **Method**: `POST`
- **URL**: `{{base_url}}/api/data/reset`
- **Headers**: None required

#### 4. Export Data
- **Method**: `GET`
- **URL**: `{{base_url}}/api/data/export`
- **Headers**: None required

#### 5. Import Data
- **Method**: `POST`
- **URL**: `{{base_url}}/api/data/import`
- **Headers**: 
  - `Content-Type: application/json`
- **Body** (raw JSON):
  ```json
  {
    "import_file": "export_20240115_123456.json"
  }
  ```

### 📋 General Operations

#### 1. API Documentation
- **Method**: `GET`
- **URL**: `{{base_url}}/`
- **Headers**: None required

#### 2. Health Check
- **Method**: `GET`
- **URL**: `{{base_url}}/health`
- **Headers**: None required

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_models
python -m unittest tests.test_routes
```

## ⚙️ Configuration

The application uses environment-based configuration:

- **Development**: Default configuration with debug enabled
- **Production**: Production settings with debug disabled
- **Testing**: Test configuration with separate data files

### Environment Variables

- `FLASK_ENV`: Set to 'production' for production mode
- `SECRET_KEY`: Secret key for the application
- `FLASK_DEBUG`: Set to 'True' to enable debug mode

## 📊 Data Models

### Book Model
```json
{
  "id": 1,
  "title": "Book Title",
  "author": "Author Name",
  "year": 2023,
  "genre": "Fiction",
  "description": "Book description",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:45:00"
}
```

### Author Model
```json
{
  "id": 1,
  "name": "Author Name",
  "birth_year": 1990,
  "death_year": null,
  "nationality": "American",
  "biography": "Author biography",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:45:00"
}
```

## 🔧 Validation Rules

### Books
- **Title**: Required, max 200 characters
- **Author**: Required, max 100 characters
- **Year**: Optional, between 1800 and current year + 1
- **Genre**: Optional, max 50 characters
- **Description**: Optional, max 1000 characters

### Authors
- **Name**: Required, max 100 characters
- **Birth Year**: Optional, between 1000 and current year
- **Death Year**: Optional, must be after birth year
- **Nationality**: Optional
- **Biography**: Optional

## 🚨 Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error message",
  "timestamp": "2024-01-15T10:30:00"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `405`: Method Not Allowed
- `500`: Internal Server Error

## 🔄 Pagination

List endpoints support pagination:

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 25,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

## 🔍 Search

Search functionality supports:
- Full-text search across title, author, genre, and description
- Minimum query length: 2 characters
- Maximum query length: 100 characters
- Case-insensitive matching
- Pagination support

## 💡 Postman Tips

### 🎯 Best Practices

1. **Use Environment Variables**: Set up `base_url` to easily switch between environments
2. **Save Responses**: Use Postman's "Save Response" feature to store important data
3. **Use Collections**: Organize your requests into collections for better management
4. **Test Scripts**: Add test scripts to validate responses automatically
5. **Pre-request Scripts**: Use to set dynamic variables like IDs

### 🔄 Workflow for Testing

1. **Start Fresh**: Use `POST /api/data/reset` to start with default data
2. **Create Data**: Use POST requests to create books and authors
3. **Test Operations**: Use GET, PUT, DELETE to test all operations
4. **Search & Filter**: Test search and filtering functionality
5. **Backup**: Use `POST /api/data/backup` to save your work
6. **Export**: Use `GET /api/data/export` to download your data

### 🎨 Response Examples

#### Successful Response
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien"
  },
  "message": "Book created successfully"
}
```

#### Error Response
```json
{
  "success": false,
  "error": "Missing required field: title"
}
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🤝 Support

For support and questions, please open an issue on GitHub.

---

**Happy API Testing! 🚀** 