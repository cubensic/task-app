import os
from app import create_app

# Get the environment from the environment variable, default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG']) 