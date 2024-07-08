# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the script into the container
COPY run.sh /code/run.sh

# Make the script executable
RUN chmod +x /code/run.sh

# Run the script when the container launches
CMD ["/code/run.sh"]