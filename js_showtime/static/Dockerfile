# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the entire project into the container
# COPY . .
COPY app.py /app

# Expose the port that the FastAPI application will run on
EXPOSE 8000

# Start the FastAPI application when the container runs
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
