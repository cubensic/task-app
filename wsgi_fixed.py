import os
from app import create_app

env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env) 