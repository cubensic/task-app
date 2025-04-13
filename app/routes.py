from flask import Blueprint, jsonify, request, render_template, abort
from app.models import db, Task

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional status filter."""
    status = request.args.get('status')
    
    if status and status in ['active', 'completed']:
        tasks = Task.query.filter_by(status=status).all()
    else:
        tasks = Task.query.all()
    
    return jsonify({
        'success': True,
        'tasks': [task.to_dict() for task in tasks]
    })

@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID."""
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    return jsonify({
        'success': True,
        'task': task.to_dict()
    })

@api_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({
            'success': False,
            'error': 'Title is required'
        }), 400
    
    new_task = Task(
        title=data['title'],
        description=data.get('description', '')
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': new_task.to_dict()
    }), 201

@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task."""
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data and data['status'] in ['active', 'completed']:
        task.status = data['status']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'task': task.to_dict()
    })

@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    task = db.session.get(Task, task_id)
    if task is None:
        abort(404)
        
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Task {task_id} deleted successfully'
    }) 