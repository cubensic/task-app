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

def test_task_lifecycle(client):
    """
    Integration test for the complete task lifecycle:
    - Create a new task
    - Verify it exists in the task list
    - Update the task
    - Verify the update was applied
    - Delete the task
    - Verify it no longer exists
    """
    # 1. Create a new task
    create_data = {
        'title': 'Integration Test Task',
        'description': 'Testing the full task lifecycle'
    }
    
    create_response = client.post(
        '/api/tasks',
        data=json.dumps(create_data),
        content_type='application/json'
    )
    
    assert create_response.status_code == 201
    create_result = json.loads(create_response.data)
    assert create_result['success'] is True
    
    # Get the task ID for later operations
    task_id = create_result['task']['id']
    
    # 2. Verify the task exists in the task list
    list_response = client.get('/api/tasks')
    assert list_response.status_code == 200
    list_result = json.loads(list_response.data)
    
    # Find our task in the list
    found_task = None
    for task in list_result['tasks']:
        if task['id'] == task_id:
            found_task = task
            break
    
    assert found_task is not None
    assert found_task['title'] == 'Integration Test Task'
    assert found_task['description'] == 'Testing the full task lifecycle'
    assert found_task['status'] == 'active'
    
    # 3. Update the task
    update_data = {
        'title': 'Updated Integration Task',
        'status': 'completed'
    }
    
    update_response = client.put(
        f'/api/tasks/{task_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    
    assert update_response.status_code == 200
    update_result = json.loads(update_response.data)
    assert update_result['success'] is True
    assert update_result['task']['title'] == 'Updated Integration Task'
    assert update_result['task']['status'] == 'completed'
    assert update_result['task']['description'] == 'Testing the full task lifecycle'  # Unchanged
    
    # 4. Verify the update was applied by getting the specific task
    get_response = client.get(f'/api/tasks/{task_id}')
    assert get_response.status_code == 200
    get_result = json.loads(get_response.data)
    
    assert get_result['task']['title'] == 'Updated Integration Task'
    assert get_result['task']['status'] == 'completed'
    
    # 5. Delete the task
    delete_response = client.delete(f'/api/tasks/{task_id}')
    assert delete_response.status_code == 200
    delete_result = json.loads(delete_response.data)
    assert delete_result['success'] is True
    
    # 6. Verify the task no longer exists
    verify_response = client.get(f'/api/tasks/{task_id}')
    assert verify_response.status_code == 404  # Task should not be found

def test_filtering_functionality(client):
    """
    Integration test for task filtering functionality:
    - Create tasks with different statuses
    - Test filtering by 'active' status
    - Test filtering by 'completed' status
    - Test filtering with 'all' (no filter)
    """
    # Create test tasks with different statuses
    with client.application.app_context():
        # Create active tasks
        for i in range(3):
            db.session.add(Task(
                title=f'Active Task {i+1}',
                description=f'Active task description {i+1}',
                status='active'
            ))
        
        # Create completed tasks
        for i in range(2):
            db.session.add(Task(
                title=f'Completed Task {i+1}',
                description=f'Completed task description {i+1}',
                status='completed'
            ))
        
        db.session.commit()
    
    # Test filtering by 'active' status
    active_response = client.get('/api/tasks?status=active')
    assert active_response.status_code == 200
    active_result = json.loads(active_response.data)
    
    assert active_result['success'] is True
    assert len(active_result['tasks']) == 3
    for task in active_result['tasks']:
        assert task['status'] == 'active'
        assert 'Active Task' in task['title']
    
    # Test filtering by 'completed' status
    completed_response = client.get('/api/tasks?status=completed')
    assert completed_response.status_code == 200
    completed_result = json.loads(completed_response.data)
    
    assert completed_result['success'] is True
    assert len(completed_result['tasks']) == 2
    for task in completed_result['tasks']:
        assert task['status'] == 'completed'
        assert 'Completed Task' in task['title']
    
    # Test retrieving all tasks (no filter)
    all_response = client.get('/api/tasks')
    assert all_response.status_code == 200
    all_result = json.loads(all_response.data)
    
    assert all_result['success'] is True
    assert len(all_result['tasks']) == 5  # 3 active + 2 completed

def test_error_handling(client):
    """
    Integration test for error handling:
    - Test invalid task creation (missing required fields)
    - Test updating a non-existent task
    - Test deleting a non-existent task
    - Test retrieving a non-existent task
    """
    # Test invalid task creation (missing title)
    invalid_create_data = {
        'description': 'Task without a title'
    }
    
    create_response = client.post(
        '/api/tasks',
        data=json.dumps(invalid_create_data),
        content_type='application/json'
    )
    
    assert create_response.status_code == 400
    create_result = json.loads(create_response.data)
    assert create_result['success'] is False
    assert 'error' in create_result
    
    # Test operations on non-existent task ID
    non_existent_id = 9999
    
    # Test updating non-existent task
    update_data = {'title': 'Updated Title'}
    update_response = client.put(
        f'/api/tasks/{non_existent_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    assert update_response.status_code == 404
    
    # Test deleting non-existent task
    delete_response = client.delete(f'/api/tasks/{non_existent_id}')
    assert delete_response.status_code == 404
    
    # Test retrieving non-existent task
    get_response = client.get(f'/api/tasks/{non_existent_id}')
    assert get_response.status_code == 404 