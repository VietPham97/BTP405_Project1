# The base image is python 3.11 slim
FROM python:3.11-slim

# Create the working directory
WORKDIR /app

# Copy all the code to the Docker image
COPY . /app

# Expose the application port
EXPOSE 8080

# Run the python server, which will return 
# Toronto current time as JSON for GET request
CMD [ "python", "server.py" ]

# Build a docker image:
# run command: docker build -t vietpham/healthcare:v1 . 
# Run a docker container:
# run command: docker run -p 8080:8080 vietpham/healthcare:v1
