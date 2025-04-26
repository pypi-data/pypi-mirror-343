# AI Planet CLI

AI Planet CLI is a powerful command-line tool for generating FastAPI project boilerplate with best practices baked in. It helps you quickly scaffold a production-ready FastAPI application with the right structure and components.

## Features

- **Project Generation**: Create a new FastAPI project with the recommended structure
- **Component Management**: Add, remove, and generate components for your project
- **Database Migrations**: Manage database migrations with Alembic
- **Development Server**: Run your FastAPI application in development or production mode
- **Docker Support**: Generate Docker configuration and run your app in containers

## Installation

```bash
pip install aiplanet
```

## Project Structure

The CLI generates a project with the following structure:

```
my_project/                      # Project root
├── my_project/                  # Main package directory
│   ├── __init__.py              # Package initialization with version
│   ├── constants/               # Application constants
│   ├── core/                    # Core functionality
│   │   ├── config.py            # Application configuration
│   │   ├── database.py          # Database connection
│   │   ├── security.py          # Authentication and authorization
│   │   └── logging.py           # Logging configuration
│   ├── exceptions/              # Custom exceptions
│   ├── jobs/                    # Background jobs
│   ├── middleware/              # Middleware components
│   ├── models/                  # SQLAlchemy models
│   ├── routers/                 # API endpoints
│   │   ├── v1/                  # API version 1
│   │   │   ├── public/          # Public endpoints
│   │   │   └── private/         # Authenticated endpoints
│   ├── schemas/                 # Pydantic schemas
│   ├── services/                # Business logic
│   └── utils/                   # Utility functions
├── tests/                       # Tests directory
├── migrations/                  # Alembic migrations
├── main.py                      # Application entry point
├── pyproject.toml               # Poetry configuration
├── alembic.ini                  # Alembic configuration
├── README.md                    # Documentation
└── .gitignore                   # Git configuration
```

## Usage

### Creating a New Project

```bash
aiplanet build project my_project --docker --github-actions
```

Options:
- `--docker`: Include Docker configuration
- `--github-actions`: Include GitHub Actions workflow
- `--pre-commit`: Include pre-commit hooks
- `--minimal`: Create a minimal project

### Adding Components

```bash
aiplanet add service user
aiplanet add model user
aiplanet add schema user
aiplanet add route user
```

### Generating Complete Modules

```bash
aiplanet gen module user --with-middleware --with-exception
```

### Managing Database Migrations

```bash
aiplanet migrate init
aiplanet migrate create "create users table"
aiplanet migrate upgrade head
```

### Running the Application

```bash
# Development server
aiplanet run dev

# Production server
aiplanet run prod --workers 4

# Docker
aiplanet run docker
```

## Component Types

- **Service**: Business logic services
- **Model**: SQLAlchemy database models
- **Schema**: Pydantic schemas for request/response
- **Route**: API endpoints (routers)
- **Job**: Background jobs/tasks
- **Middleware**: ASGI middleware components
- **Const**: Constant definitions
- **Utils**: Utility functions
- **Exception**: Custom exception classes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.