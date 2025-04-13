import pytest
from app import create_app
from app.models import db, Task
from datetime import datetime
import time

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

@pytest.fixture
def task_instance():
    """Create a task instance without saving to DB."""
    return Task(title='Test Task', description='Test Description')

def test_task_creation(app, task_instance):
    """Test creating a new task."""
    with app.app_context():
        # Add to database and verify
        db.session.add(task_instance)
        db.session.commit()
        
        # Retrieve from database and verify
        saved_task = Task.query.filter_by(title='Test Task').first()
        assert saved_task is not None
        assert saved_task.title == 'Test Task'
        assert saved_task.description == 'Test Description'
        assert saved_task.status == 'active'  # Check status after database save

def test_task_update(app):
    """Test updating a task."""
    with app.app_context():
        # Create and save a task
        task = Task(title='Original Title', description='Original Description')
        db.session.add(task)
        db.session.commit()
        
        # Get ID for later retrieval
        task_id = task.id
        
        # Update the task
        task.title = 'Updated Title'
        task.description = 'Updated Description'
        task.status = 'completed'
        db.session.commit()
        
        # Retrieve updated task and verify changes
        updated_task = Task.query.get(task_id)
        assert updated_task.title == 'Updated Title'
        assert updated_task.description == 'Updated Description'
        assert updated_task.status == 'completed'

def test_task_deletion(app):
    """Test deleting a task."""
    with app.app_context():
        # Create and save a task
        task = Task(title='Delete Me', description='To be deleted')
        db.session.add(task)
        db.session.commit()
        
        # Get ID for later check
        task_id = task.id
        
        # Delete the task
        db.session.delete(task)
        db.session.commit()
        
        # Verify task no longer exists
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None

def test_timestamps(app):
    """Test that created_at and updated_at timestamps are working."""
    with app.app_context():
        # Create a new task
        task = Task(title='Timestamp Test', description='Testing timestamps')
        db.session.add(task)
        db.session.commit()
        
        # Verify created_at is set
        assert task.created_at is not None
        original_created_at = task.created_at
        
        # Small delay to ensure timestamps would be different
        time.sleep(0.1)
        
        # Update the task
        task.title = 'Updated Timestamp'
        db.session.commit()
        
        # Verify updated_at changed but created_at didn't
        assert task.updated_at > original_created_at
        assert task.created_at == original_created_at

def test_default_values(app):
    """Test default values for task fields."""
    with app.app_context():
        # Create task with minimal fields
        task = Task(title='Minimal Task')
        db.session.add(task)
        db.session.commit()
        
        # Verify defaults
        assert task.description is None  # No description provided
        assert task.status == 'active'   # Default status
        assert task.created_at is not None  # Timestamp automatically set

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