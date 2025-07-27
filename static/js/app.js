// Book API Frontend Application
class BookAPIApp {
    constructor() {
        this.baseURL = window.location.origin;
        this.currentUser = null;
        this.accessToken = localStorage.getItem('accessToken');
        this.currentPage = 1;
        this.searchQuery = '';
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        this.loadHomePage();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.dataset.page;
                this.navigateToPage(page);
            });
        });

        // Logout
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.logout();
        });

        // Search
        document.getElementById('searchForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.searchBooks();
        });

        document.getElementById('clearSearch').addEventListener('click', () => {
            this.clearSearch();
        });

        // Pagination
        document.getElementById('prevPage').addEventListener('click', () => {
            this.currentPage--;
            this.loadBooks();
        });

        document.getElementById('nextPage').addEventListener('click', () => {
            this.currentPage++;
            this.loadBooks();
        });

        // Book modals
        document.getElementById('addBookBtn').addEventListener('click', () => {
            this.showBookModal();
        });

        document.getElementById('saveBookModal').addEventListener('click', () => {
            this.saveBook();
        });

        document.getElementById('closeBookModal').addEventListener('click', () => {
            this.hideBookModal();
        });

        document.getElementById('cancelBookModal').addEventListener('click', () => {
            this.hideBookModal();
        });

        // Author modals
        document.getElementById('addAuthorBtn').addEventListener('click', () => {
            this.showAuthorModal();
        });

        document.getElementById('saveAuthorModal').addEventListener('click', () => {
            this.saveAuthor();
        });

        document.getElementById('closeAuthorModal').addEventListener('click', () => {
            this.hideAuthorModal();
        });

        document.getElementById('cancelAuthorModal').addEventListener('click', () => {
            this.hideAuthorModal();
        });

        // Forms
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });

        document.getElementById('updateProfileForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.updateProfile();
        });

        // Modal overlay clicks
        document.getElementById('bookModal').addEventListener('click', (e) => {
            if (e.target.id === 'bookModal') {
                this.hideBookModal();
            }
        });

        document.getElementById('authorModal').addEventListener('click', (e) => {
            if (e.target.id === 'authorModal') {
                this.hideAuthorModal();
            }
        });
    }

    // Navigation
    navigateToPage(page) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
        
        // Remove active class from all nav links
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        
        // Show target page and activate nav link
        const targetPage = document.getElementById(page + 'Page');
        const targetLink = document.querySelector(`[data-page="${page}"]`);
        
        if (targetPage) {
            targetPage.classList.remove('hidden');
            targetPage.classList.add('active');
        }
        
        if (targetLink) {
            targetLink.classList.add('active');
        }

        // Load page-specific content
        switch (page) {
            case 'home':
                this.loadHomePage();
                break;
            case 'books':
                this.loadBooks();
                break;
            case 'authors':
                this.loadAuthors();
                break;
            case 'profile':
                this.loadProfile();
                break;
        }
    }

    // Authentication
    async checkAuthStatus() {
        if (this.accessToken) {
            try {
                const response = await this.apiCall('/api/auth/profile', 'GET');
                if (response.success) {
                    this.currentUser = response.data;
                    this.updateAuthUI(true);
                } else {
                    this.logout();
                }
            } catch (error) {
                this.logout();
            }
        } else {
            this.updateAuthUI(false);
        }
    }

    updateAuthUI(isAuthenticated) {
        const loginLink = document.getElementById('loginLink');
        const profileLink = document.getElementById('profileLink');
        const logoutBtn = document.getElementById('logoutBtn');
        const addBookSection = document.getElementById('addBookSection');
        const addAuthorSection = document.getElementById('addAuthorSection');

        if (isAuthenticated) {
            loginLink.style.display = 'none';
            profileLink.classList.remove('hidden');
            logoutBtn.style.display = 'inline-flex';
            
            // Show admin/moderator features
            if (this.currentUser.role === 'admin' || this.currentUser.role === 'moderator') {
                addBookSection.style.display = 'block';
                addAuthorSection.style.display = 'block';
            }
        } else {
            loginLink.style.display = 'inline-flex';
            profileLink.classList.add('hidden');
            logoutBtn.style.display = 'none';
            addBookSection.style.display = 'none';
            addAuthorSection.style.display = 'none';
        }
    }

    async login() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await this.apiCall('/api/auth/login', 'POST', {
                username,
                password
            });

            if (response.success) {
                this.accessToken = response.data.tokens.access_token;
                localStorage.setItem('accessToken', this.accessToken);
                this.currentUser = response.data.user;
                this.updateAuthUI(true);
                this.showAlert('Login successful!', 'success');
                this.navigateToPage('home');
            } else {
                this.showAlert(response.error || 'Login failed', 'error');
            }
        } catch (error) {
            this.showAlert('Login failed. Please try again.', 'error');
        }
    }

    async register() {
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;

        try {
            const response = await this.apiCall('/api/auth/register', 'POST', {
                username,
                email,
                password
            });

            if (response.success) {
                this.showAlert('Registration successful! Please login.', 'success');
                this.navigateToPage('login');
            } else {
                this.showAlert(response.error || 'Registration failed', 'error');
            }
        } catch (error) {
            this.showAlert('Registration failed. Please try again.', 'error');
        }
    }

    async logout() {
        try {
            if (this.accessToken) {
                await this.apiCall('/api/auth/logout', 'POST');
            }
        } catch (error) {
            // Ignore logout errors
        }

        this.accessToken = null;
        this.currentUser = null;
        localStorage.removeItem('accessToken');
        this.updateAuthUI(false);
        this.showAlert('Logged out successfully', 'success');
        this.navigateToPage('home');
    }

    async loadProfile() {
        if (!this.currentUser) {
            this.navigateToPage('login');
            return;
        }

        try {
            const response = await this.apiCall('/api/auth/profile', 'GET');
            if (response.success) {
                this.displayProfile(response.data);
            }
        } catch (error) {
            this.showAlert('Failed to load profile', 'error');
        }
    }

    displayProfile(profile) {
        const profileInfo = document.getElementById('profileInfo');
        profileInfo.innerHTML = `
            <div class="mb-4">
                <strong>Username:</strong> ${profile.username}
            </div>
            <div class="mb-4">
                <strong>Email:</strong> ${profile.email}
            </div>
            <div class="mb-4">
                <strong>Role:</strong> <span class="badge" style="background: var(--primary-color); color: white; padding: 4px 8px; border-radius: 4px;">${profile.role}</span>
            </div>
            <div class="mb-4">
                <strong>Member since:</strong> ${new Date(profile.created_at).toLocaleDateString()}
            </div>
        `;

        // Pre-fill update form
        document.getElementById('updateEmail').value = profile.email;
    }

    async updateProfile() {
        const email = document.getElementById('updateEmail').value;
        const password = document.getElementById('updatePassword').value;

        const updateData = { email };
        if (password) {
            updateData.password = password;
        }

        try {
            const response = await this.apiCall('/api/auth/profile', 'PUT', updateData);
            if (response.success) {
                this.showAlert('Profile updated successfully', 'success');
                this.loadProfile();
            } else {
                this.showAlert(response.error || 'Update failed', 'error');
            }
        } catch (error) {
            this.showAlert('Update failed. Please try again.', 'error');
        }
    }

    // Books
    async loadBooks() {
        const loading = document.getElementById('booksLoading');
        const grid = document.getElementById('booksGrid');
        const pagination = document.getElementById('pagination');

        loading.classList.remove('hidden');
        grid.innerHTML = '';

        try {
            const params = new URLSearchParams({
                page: this.currentPage
            });

            if (this.searchQuery) {
                params.append('q', this.searchQuery);
            }

            const response = await this.apiCall(`/api/books?${params}`, 'GET');
            
            if (response.success) {
                this.displayBooks(response.data.books);
                this.updatePagination(response.data);
            } else {
                this.showAlert('Failed to load books', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to load books', 'error');
        } finally {
            loading.classList.add('hidden');
        }
    }

    displayBooks(books) {
        const grid = document.getElementById('booksGrid');
        grid.innerHTML = '';

        if (books.length === 0) {
            grid.innerHTML = `
                <div class="text-center" style="grid-column: 1 / -1; padding: 2rem;">
                    <i class="fas fa-book" style="font-size: 3rem; color: var(--gray-400); margin-bottom: 1rem;"></i>
                    <h3>No books found</h3>
                    <p>Try adjusting your search criteria</p>
                </div>
            `;
            return;
        }

        books.forEach(book => {
            const card = document.createElement('div');
            card.className = 'book-card';
            card.innerHTML = `
                <div class="book-image">
                    <i class="fas fa-book"></i>
                </div>
                <div class="book-content">
                    <h3 class="book-title">${this.escapeHtml(book.title)}</h3>
                    <div class="book-author">by ${this.escapeHtml(book.author)}</div>
                    <div class="book-meta">
                        ${book.year ? `<span><i class="fas fa-calendar"></i> ${book.year}</span>` : ''}
                        ${book.genre ? `<span class="book-genre">${this.escapeHtml(book.genre)}</span>` : ''}
                    </div>
                    ${book.description ? `<p class="book-description">${this.escapeHtml(book.description)}</p>` : ''}
                    <div class="book-actions">
                        <button class="btn btn-primary btn-sm" onclick="app.viewBook(${book.id})">
                            <i class="fas fa-eye"></i> View
                        </button>
                        ${this.canEditBook() ? `
                            <button class="btn btn-secondary btn-sm" onclick="app.editBook(${book.id})">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button class="btn btn-danger btn-sm" onclick="app.deleteBook(${book.id})">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        ` : ''}
                    </div>
                </div>
            `;
            grid.appendChild(card);
        });
    }

    updatePagination(data) {
        const pagination = document.getElementById('pagination');
        const pageInfo = document.getElementById('pageInfo');
        const prevBtn = document.getElementById('prevPage');
        const nextBtn = document.getElementById('nextPage');

        if (data.total_pages > 1) {
            pagination.style.display = 'block';
            pageInfo.textContent = `Page ${data.current_page} of ${data.total_pages}`;
            prevBtn.disabled = data.current_page <= 1;
            nextBtn.disabled = data.current_page >= data.total_pages;
        } else {
            pagination.style.display = 'none';
        }
    }

    searchBooks() {
        this.searchQuery = document.getElementById('searchInput').value.trim();
        this.currentPage = 1;
        this.loadBooks();
    }

    clearSearch() {
        document.getElementById('searchInput').value = '';
        this.searchQuery = '';
        this.currentPage = 1;
        this.loadBooks();
    }

    showBookModal(book = null) {
        const modal = document.getElementById('bookModal');
        const title = document.getElementById('bookModalTitle');
        const form = document.getElementById('bookForm');

        if (book) {
            title.textContent = 'Edit Book';
            document.getElementById('bookId').value = book.id;
            document.getElementById('bookTitle').value = book.title;
            document.getElementById('bookAuthor').value = book.author;
            document.getElementById('bookYear').value = book.year || '';
            document.getElementById('bookGenre').value = book.genre || '';
            document.getElementById('bookDescription').value = book.description || '';
        } else {
            title.textContent = 'Add New Book';
            form.reset();
            document.getElementById('bookId').value = '';
        }

        modal.classList.remove('hidden');
    }

    hideBookModal() {
        document.getElementById('bookModal').classList.add('hidden');
    }

    async saveBook() {
        const formData = {
            title: document.getElementById('bookTitle').value,
            author: document.getElementById('bookAuthor').value,
            year: document.getElementById('bookYear').value || null,
            genre: document.getElementById('bookGenre').value || '',
            description: document.getElementById('bookDescription').value || ''
        };

        const bookId = document.getElementById('bookId').value;
        const method = bookId ? 'PUT' : 'POST';
        const url = bookId ? `/api/books/${bookId}` : '/api/books';

        try {
            const response = await this.apiCall(url, method, formData);
            if (response.success) {
                this.showAlert(bookId ? 'Book updated successfully' : 'Book created successfully', 'success');
                this.hideBookModal();
                this.loadBooks();
            } else {
                this.showAlert(response.error || 'Failed to save book', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to save book', 'error');
        }
    }

    async deleteBook(bookId) {
        if (!confirm('Are you sure you want to delete this book?')) {
            return;
        }

        try {
            const response = await this.apiCall(`/api/books/${bookId}`, 'DELETE');
            if (response.success) {
                this.showAlert('Book deleted successfully', 'success');
                this.loadBooks();
            } else {
                this.showAlert(response.error || 'Failed to delete book', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to delete book', 'error');
        }
    }

    // Authors
    async loadAuthors() {
        const loading = document.getElementById('authorsLoading');
        const tableBody = document.getElementById('authorsTableBody');

        loading.classList.remove('hidden');
        tableBody.innerHTML = '';

        try {
            const response = await this.apiCall('/api/authors', 'GET');
            
            if (response.success) {
                this.displayAuthors(response.data);
            } else {
                this.showAlert('Failed to load authors', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to load authors', 'error');
        } finally {
            loading.classList.add('hidden');
        }
    }

    displayAuthors(authors) {
        const tableBody = document.getElementById('authorsTableBody');

        if (authors.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="text-center" style="padding: 2rem;">
                        <i class="fas fa-users" style="font-size: 2rem; color: var(--gray-400); margin-bottom: 1rem;"></i>
                        <p>No authors found</p>
                    </td>
                </tr>
            `;
            return;
        }

        authors.forEach(author => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${this.escapeHtml(author.name)}</strong></td>
                <td>${this.escapeHtml(author.biography || 'No biography available')}</td>
                <td>${author.books_count || 0}</td>
                <td>
                    <div class="book-actions">
                        <button class="btn btn-primary btn-sm" onclick="app.viewAuthor(${author.id})">
                            <i class="fas fa-eye"></i> View
                        </button>
                        ${this.canEditAuthor() ? `
                            <button class="btn btn-secondary btn-sm" onclick="app.editAuthor(${author.id})">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button class="btn btn-danger btn-sm" onclick="app.deleteAuthor(${author.id})">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        ` : ''}
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    showAuthorModal(author = null) {
        const modal = document.getElementById('authorModal');
        const title = document.getElementById('authorModalTitle');
        const form = document.getElementById('authorForm');

        if (author) {
            title.textContent = 'Edit Author';
            document.getElementById('authorId').value = author.id;
            document.getElementById('authorName').value = author.name;
            document.getElementById('authorBiography').value = author.biography || '';
        } else {
            title.textContent = 'Add New Author';
            form.reset();
            document.getElementById('authorId').value = '';
        }

        modal.classList.remove('hidden');
    }

    hideAuthorModal() {
        document.getElementById('authorModal').classList.add('hidden');
    }

    async saveAuthor() {
        const formData = {
            name: document.getElementById('authorName').value,
            biography: document.getElementById('authorBiography').value || ''
        };

        const authorId = document.getElementById('authorId').value;
        const method = authorId ? 'PUT' : 'POST';
        const url = authorId ? `/api/authors/${authorId}` : '/api/authors';

        try {
            const response = await this.apiCall(url, method, formData);
            if (response.success) {
                this.showAlert(authorId ? 'Author updated successfully' : 'Author created successfully', 'success');
                this.hideAuthorModal();
                this.loadAuthors();
            } else {
                this.showAlert(response.error || 'Failed to save author', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to save author', 'error');
        }
    }

    async deleteAuthor(authorId) {
        if (!confirm('Are you sure you want to delete this author?')) {
            return;
        }

        try {
            const response = await this.apiCall(`/api/authors/${authorId}`, 'DELETE');
            if (response.success) {
                this.showAlert('Author deleted successfully', 'success');
                this.loadAuthors();
            } else {
                this.showAlert(response.error || 'Failed to delete author', 'error');
            }
        } catch (error) {
            this.showAlert('Failed to delete author', 'error');
        }
    }

    // Home page
    async loadHomePage() {
        try {
            const [booksResponse, authorsResponse, healthResponse] = await Promise.all([
                this.apiCall('/api/books', 'GET'),
                this.apiCall('/api/authors', 'GET'),
                this.apiCall('/health', 'GET')
            ]);

            if (booksResponse.success) {
                document.getElementById('totalBooks').textContent = booksResponse.data.total || 0;
            }

            if (authorsResponse.success) {
                document.getElementById('totalAuthors').textContent = authorsResponse.data.count || 0;
            }

            if (healthResponse.status === 'healthy') {
                document.getElementById('apiStatus').textContent = 'Online';
                document.getElementById('apiStatus').style.color = 'var(--success-color)';
            } else {
                document.getElementById('apiStatus').textContent = 'Offline';
                document.getElementById('apiStatus').style.color = 'var(--error-color)';
            }
        } catch (error) {
            document.getElementById('apiStatus').textContent = 'Offline';
            document.getElementById('apiStatus').style.color = 'var(--error-color)';
        }
    }

    // Utility methods
    async apiCall(endpoint, method = 'GET', data = null) {
        const url = this.baseURL + endpoint;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (this.accessToken) {
            options.headers['Authorization'] = `Bearer ${this.accessToken}`;
        }

        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }

        return result;
    }

    showAlert(message, type = 'info') {
        const container = document.getElementById('alertContainer');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} fade-in`;
        alert.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer; font-size: 1.2rem;">×</button>
            </div>
        `;

        container.appendChild(alert);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 5000);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    canEditBook() {
        return this.currentUser && (this.currentUser.role === 'admin' || this.currentUser.role === 'moderator');
    }

    canEditAuthor() {
        return this.currentUser && (this.currentUser.role === 'admin' || this.currentUser.role === 'moderator');
    }

    // Placeholder methods for future implementation
    viewBook(id) {
        this.showAlert(`View book ${id} - Feature coming soon!`, 'info');
    }

    editBook(id) {
        // Load book data and show modal
        this.apiCall(`/api/books/${id}`, 'GET').then(response => {
            if (response.success) {
                this.showBookModal(response.data);
            }
        });
    }

    viewAuthor(id) {
        this.showAlert(`View author ${id} - Feature coming soon!`, 'info');
    }

    editAuthor(id) {
        // Load author data and show modal
        this.apiCall(`/api/authors/${id}`, 'GET').then(response => {
            if (response.success) {
                this.showAuthorModal(response.data);
            }
        });
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BookAPIApp();
}); 