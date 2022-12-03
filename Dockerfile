# Image
FROM python:3.8-slim-buster

# Work directory
WORKDIR /app

# Requirements & Installations
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run
CMD ["gunicorn", "app:app"]

# Expose port
EXPOSE 5003