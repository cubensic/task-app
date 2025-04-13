import pytest
from app import create_app
from app.models import db, Task
from datetime import datetime

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    # Create all tables in the test database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_create_task(app):
    """Test Task model creation."""
    with app.app_context():
        # Create a new task
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        
        # Retrieve the task from the database
        saved_task = Task.query.filter_by(title='Test Task').first()
        
        # Assertions
        assert saved_task is not None
        assert saved_task.title == 'Test Task'
        assert saved_task.description == 'Test Description'
        assert saved_task.status == 'active'  # Default status
        assert isinstance(saved_task.created_at, datetime)
        
def test_task_to_dict(app):
    """Test Task to_dict method."""
    with app.app_context():
        # Create a new task
        task = Task(title='Dict Test', description='Testing to_dict method')
        db.session.add(task)
        db.session.commit()
        
        # Get the dictionary representation
        task_dict = task.to_dict()
        
        # Assertions
        assert task_dict['id'] == task.id
        assert task_dict['title'] == 'Dict Test'
        assert task_dict['description'] == 'Testing to_dict method'
        assert task_dict['status'] == 'active'
        assert task_dict['created_at'] is not None 