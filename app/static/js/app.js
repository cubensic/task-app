document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const taskForm = document.getElementById('task-form');
    const tasksList = document.getElementById('tasks');
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    // Current filter state
    let currentFilter = 'all';
    
    // Fetch all tasks on page load
    fetchTasks();
    
    // Event Listeners
    taskForm.addEventListener('submit', createTask);
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.getAttribute('data-filter');
            setActiveFilter(filter);
            fetchTasks(filter);
        });
    });
    
    // Functions
    
    function fetchTasks(filter = 'all') {
        let url = '/api/tasks';
        
        if (filter !== 'all') {
            url += '?status=' + filter;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    renderTasks(data.tasks);
                }
            })
            .catch(error => console.error('Error fetching tasks:', error));
    }
    
    function createTask(e) {
        e.preventDefault();
        
        const titleInput = document.getElementById('task-title');
        const descriptionInput = document.getElementById('task-description');
        
        const taskData = {
            title: titleInput.value,
            description: descriptionInput.value
        };
        
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear form
                titleInput.value = '';
                descriptionInput.value = '';
                
                // Refresh tasks
                fetchTasks(currentFilter);
            }
        })
        .catch(error => console.error('Error creating task:', error));
    }
    
    function updateTask(taskId, updatedData) {
        fetch(`/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchTasks(currentFilter);
            }
        })
        .catch(error => console.error('Error updating task:', error));
    }
    
    function deleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    fetchTasks(currentFilter);
                }
            })
            .catch(error => console.error('Error deleting task:', error));
        }
    }
    
    function toggleTaskStatus(taskId, currentStatus) {
        const newStatus = currentStatus === 'active' ? 'completed' : 'active';
        updateTask(taskId, { status: newStatus });
    }
    
    function renderTasks(tasks) {
        tasksList.innerHTML = '';
        
        if (tasks.length === 0) {
            tasksList.innerHTML = '<li class="task-item"><p class="empty-message">No tasks found.</p></li>';
            return;
        }
        
        tasks.forEach(task => {
            const taskElement = document.createElement('li');
            taskElement.className = `task-item ${task.status === 'completed' ? 'completed' : ''}`;
            
            taskElement.innerHTML = `
                <div class="task-checkbox">
                    <input type="checkbox" id="task-${task.id}" ${task.status === 'completed' ? 'checked' : ''}>
                </div>
                <div class="task-content">
                    <h3 class="task-title">${task.title}</h3>
                    ${task.description ? `<p class="task-description">${task.description}</p>` : ''}
                </div>
                <div class="task-actions">
                    <button class="task-edit" data-id="${task.id}">Edit</button>
                    <button class="task-delete" data-id="${task.id}">Delete</button>
                </div>
            `;
            
            tasksList.appendChild(taskElement);
            
            // Add event listeners to the newly created elements
            const checkbox = taskElement.querySelector(`#task-${task.id}`);
            checkbox.addEventListener('change', function() {
                toggleTaskStatus(task.id, task.status);
            });
            
            const editButton = taskElement.querySelector('.task-edit');
            editButton.addEventListener('click', function() {
                // Simple implementation: prompt for new title
                const newTitle = prompt('Update task title:', task.title);
                const newDescription = prompt('Update task description:', task.description);
                
                if (newTitle !== null && newTitle.trim() !== '') {
                    updateTask(task.id, { 
                        title: newTitle,
                        description: newDescription
                    });
                }
            });
            
            const deleteButton = taskElement.querySelector('.task-delete');
            deleteButton.addEventListener('click', function() {
                deleteTask(task.id);
            });
        });
    }
    
    function setActiveFilter(filter) {
        currentFilter = filter;
        
        filterButtons.forEach(button => {
            if (button.getAttribute('data-filter') === filter) {
                button.classList.add('active');
            } else {
                button.classList.remove('active');
            }
        });
    }
}); 