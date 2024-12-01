# Use an official Python runtime as a parent image
 # Check your python version for this
 FROM python:3.12.2

 # Set the working directory to /app
 WORKDIR /app

 # Copy the current directory contents into the container at /app
 COPY . /app

 # Install any needed packages specified in requirements.txt
 RUN pip install --no-cache-dir -r requirements.txt

 # Create a volume for the SQLite database
 VOLUME /app/data

 # Make port 5000 available to the world outside this container
 EXPOSE 5000

 # Set environment variable FLASK_APP
 # my app is in app.py, your might be different
 ENV FLASK_APP=predictor.py

 # Run app.py when the container launches
 CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]