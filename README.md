# Book Management System

## Objective
The **Book Management System** is a FastAPI-based backend that manages books and authors, utilizing a PostgreSQL database. It provides authentication, CRUD operations, bulk import capabilities, and advanced filtering, pagination, and sorting.

## Features
- **User Authentication** (JWT-based authentication for secured access)
- **Book Management** (CRUD operations, pagination, and sorting)
- **Author Management** (CRUD operations)
- **Bulk Import** (Supports JSON/CSV file uploads for book data)
- **Database Interaction** (Uses raw SQL queries and stored procedures)

## API Endpoints

### Authentication
- `POST /auth/jwt/create` - Authenticate user and generate JWT tokens.

### User Management
- `POST /user/register` - Register a new user.

### Author Management
- `GET /author/` - Retrieve all authors.
- `GET /author/{author_id}` - Retrieve a specific author.
- `POST /author/` - Create a new author.
- `PUT /author/{author_id}` - Update an existing author.
- `DELETE /author/{author_id}` - Delete an author.

### Book Management
- `POST /book/` - Create a new book.
- `GET /book/` - Retrieve all books (with filters, pagination, and sorting).
- `GET /book/{book_id}` - Retrieve a specific book.
- `PUT /book/{book_id}` - Update an existing book.
- `DELETE /book/{book_id}` - Delete a book.
- `POST /book/import` - Bulk import books from JSON or CSV.

## Project Setup

### Prerequisites
Ensure you have the following installed:
- **Docker & Docker Compose**
- **Python 3.12**
- **PostgreSQL**

### Running with Docker Compose
The project includes a `docker-compose.yml` file that sets up the FastAPI application and the PostgreSQL database.

#### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/book-management-system.git
   cd book-management-system
   ```
2. Create an `.env` file and configure the following variables:
   ```env
   # Database configuration for main environment
    DATABASE_URL=postgresql+asyncpg://<your_user>:<your_password>@localhost:<your_port>/<your_db_name>
    
    # Database configuration for testing environment
    DATABASE_TEST_URL=postgresql+asyncpg://<your_user>:<your_password>@localhost:<your_test_port>/<your_test_db_name>
    
    # Secret key for encryption and session management
    SECRET_KEY=<your_secret_key>
    
    # JWT algorithm used for token encoding
    ALGORITHM=HS256
    
    # PostgreSQL environment variables for main environment
    POSTGRES_USER=<your_user>
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_DB=<your_db_name>
    
    # PostgreSQL environment variables for testing environment
    TEST_POSTGRES_USER=<your_test_user>
    TEST_POSTGRES_PASSWORD=<your_test_password>
    TEST_POSTGRES_DB=<your_test_db_name>

   ```
3. Start the containers:
   ```bash
   docker-compose up --build
   ```
4. Access the API documentation at:
   - OpenAPI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Running Tests
To run unit and integration tests:
```bash
pytest
```

## License
This project is licensed under the MIT License.
