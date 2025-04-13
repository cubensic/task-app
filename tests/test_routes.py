import pytest
import json
from app import create_app
from app.models import db, Task

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
def sample_task(app):
    """Create a sample task for testing and return its ID."""
    with app.app_context():
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        # Return the task ID rather than the task object to avoid detached instance errors
        return task.id

def test_get_all_tasks(client):
    """Test GET /api/tasks endpoint."""
    # Create some test tasks
    with client.application.app_context():
        db.session.add(Task(title='Task 1', description='Description 1'))
        db.session.add(Task(title='Task 2', description='Description 2'))
        db.session.commit()
    
    # Make the request
    response = client.get('/api/tasks')
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['tasks']) == 2
    assert data['tasks'][0]['title'] == 'Task 1'
    assert data['tasks'][1]['title'] == 'Task 2'

def test_get_tasks_with_status_filter(client):
    """Test GET /api/tasks with status filter."""
    # Create test tasks with different statuses
    with client.application.app_context():
        db.session.add(Task(title='Active Task', description='Active', status='active'))
        db.session.add(Task(title='Completed Task', description='Done', status='completed'))
        db.session.commit()
    
    # Make the request with filter
    response = client.get('/api/tasks?status=completed')
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['title'] == 'Completed Task'
    assert data['tasks'][0]['status'] == 'completed'

def test_get_single_task(client, sample_task):
    """Test GET /api/tasks/{id} endpoint."""
    # Make the request using the task ID returned by the fixture
    response = client.get(f'/api/tasks/{sample_task}')
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    assert data['task']['id'] == sample_task
    assert data['task']['title'] == 'Test Task'
    assert data['task']['description'] == 'Test Description'

def test_get_nonexistent_task(client):
    """Test GET /api/tasks/{id} with non-existent ID."""
    # Make the request with a non-existent ID
    response = client.get('/api/tasks/999')
    
    # Assertions
    assert response.status_code == 404

def test_create_task(client):
    """Test POST /api/tasks endpoint."""
    # Task data
    task_data = {
        'title': 'New Task',
        'description': 'New Description'
    }
    
    # Make the request
    response = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 201
    assert data['success'] is True
    assert data['task']['title'] == 'New Task'
    assert data['task']['description'] == 'New Description'
    assert data['task']['status'] == 'active'
    
    # Check that task was actually added to database
    with client.application.app_context():
        task = Task.query.filter_by(title='New Task').first()
        assert task is not None
        assert task.description == 'New Description'

def test_create_task_without_title(client):
    """Test POST /api/tasks with missing title."""
    # Task data without title
    task_data = {
        'description': 'No Title Description'
    }
    
    # Make the request
    response = client.post(
        '/api/tasks',
        data=json.dumps(task_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 400
    assert data['success'] is False
    assert 'error' in data

def test_update_task(client, sample_task):
    """Test PUT /api/tasks/{id} endpoint."""
    # Update data
    update_data = {
        'title': 'Updated Title',
        'status': 'completed'
    }
    
    # Make the request using the task ID returned by the fixture
    response = client.put(
        f'/api/tasks/{sample_task}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    assert data['task']['title'] == 'Updated Title'
    assert data['task']['status'] == 'completed'
    
    # Check that task was actually updated in database
    with client.application.app_context():
        task = Task.query.get(sample_task)
        assert task.title == 'Updated Title'
        assert task.status == 'completed'

def test_update_nonexistent_task(client):
    """Test PUT /api/tasks/{id} with non-existent ID."""
    # Update data
    update_data = {
        'title': 'Updated Title'
    }
    
    # Make the request with a non-existent ID
    response = client.put(
        '/api/tasks/999',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    # Assertions
    assert response.status_code == 404

def test_delete_task(client, sample_task):
    """Test DELETE /api/tasks/{id} endpoint."""
    # Make the request using the task ID returned by the fixture
    response = client.delete(f'/api/tasks/{sample_task}')
    data = json.loads(response.data)
    
    # Assertions
    assert response.status_code == 200
    assert data['success'] is True
    
    # Check that task was actually deleted from database
    with client.application.app_context():
        task = Task.query.get(sample_task)
        assert task is None

def test_delete_nonexistent_task(client):
    """Test DELETE /api/tasks/{id} with non-existent ID."""
    # Make the request with a non-existent ID
    response = client.delete('/api/tasks/999')
    
    # Assertions
    assert response.status_code == 404 