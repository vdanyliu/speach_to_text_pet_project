
---
## Description
Text to speach fastapi backend service

## Requirements
Make sure you have Python installed. If not, download and install it from Python's official website: https://www.python.org/.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/vdanyliu/speach_to_text_pet_project.git
   cd eve_call_test_task
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application locally, use the following command:
```
uvicorn runapp:app ${UVICORN_OPTS} --host 0.0.0.0 --port ${SERVICE_PORT}
```
Access the API documentation at /docs after the host address.
## Docker Usage
1. Build the Docker image:
   ```
   docker build -f ./docker/Dockerfile -t some_container_name .
   ```

2. Run the Docker container:
   ```
   docker run -p 8080:8080 -v ${ABSOLUTE_PATH_TO_JSON}:/app/google_credentials.json --name some_container_name some_container_name
   ```

Replace `${ABSOLUTE_PATH_TOJSON}` with the absolute path to your `google_credentials.json` file.

Access the API documentation at /docs after the host address.

---
