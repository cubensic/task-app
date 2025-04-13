FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Force rebuild
RUN echo "Rebuild on $(date)"

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Debugging - echo environment variables
RUN echo "Environment check"
RUN printenv | grep -E 'DATABASE|FLASK|SQLALCHEMY'

# Start gunicorn with more detailed logging
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "debug", "wsgi:app"] 