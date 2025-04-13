# To-Do List Application

A simple to-do list web application built with Flask and vanilla JavaScript. This application allows users to create, view, update, and delete tasks in a clean, minimalist interface.

## Features

- Create new tasks with title and optional description
- View all tasks in a list format
- Mark tasks as complete or active
- Edit existing task details
- Delete tasks
- Filter tasks by status (All/Active/Completed)
- Responsive design that works on both mobile and desktop

## Project Structure

```
Todo-List-App/
│
├── app/                    # Application package
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── task.py
│   ├── static/             # Static files
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── app.js
│   ├── templates/          # HTML templates
│   │   └── index.html
│   ├── __init__.py         # Application factory
│   └── routes.py           # API routes
│
├── config/                 # Configuration
│   └── config.py
│
├── tests/                  # Test package
│
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── app.py                  # Application entry point
├── README.md               # This file
└── requirements.txt        # Dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd todo-list-app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables (or use the provided .env file)

5. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Running the Application

1. Start the development server:
   ```
   python app.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Development

### Environment Configuration

The application has three environments:

- **Development**: Uses SQLite, enables debugging
- **Testing**: Uses a separate SQLite database for testing
- **Production**: Configured for PostgreSQL, disables debugging

### Database Migrations

After making changes to the database models:

```
flask db migrate -m "Description of changes"
flask db upgrade
```

## Testing

Run the tests using pytest:

```
pytest
```

## Deployment

For production deployment:

1. Set up environment variables for production
2. Configure PostgreSQL
3. Run with a production WSGI server (Gunicorn)

## License

[MIT License](LICENSE) 