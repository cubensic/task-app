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

# Run database migrations
RUN flask db upgrade

# Expose port
EXPOSE 5000

# Start gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"] 