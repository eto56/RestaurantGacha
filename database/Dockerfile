# This Dockerfile is for a one-time job to initialize the database.
FROM python:3.12-alpine

WORKDIR /app

# Install system dependencies that might be needed by Python packages
RUN apk add --no-cache postgresql-dev gcc musl-dev

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files needed for the scripts
# This includes the database scripts, the data fetching script, and the data itself.
COPY . .

# The default command is to run the init_db.py script.
# You can override this command in Railway to run other scripts,
# for example, to run hotpepperAPI.py to refresh the data.
CMD ["python", "database/init_db.py"]
