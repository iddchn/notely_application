# Notely

Notely is a full-stack application designed to manage notes efficiently. It integrates a Flask-based backend with a frontend (located in the `notely-front` directory). The project is containerized using Docker and supports continuous integration and deployment using Jenkins.

## Features

- Flask backend for note management
- Frontend for user interaction
- Dockerized for seamless deployment
- CI/CD pipeline using Jenkins

## Prerequisites

Ensure the following are installed on your system:

- Python (version 3.8 or above)
- Docker and Docker Compose
- Node.js and npm (for frontend development)
- Git

## Installation

### Backend

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd app/flask-notely
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend:
   ```bash
   flask run
   ```

### Frontend

1. Navigate to the `notely-front` directory:
   ```bash
   cd notely-front
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Usage

1. Access the application:
   - Backend: `http://localhost:5001`
   - Frontend: `http://localhost:3000`

2. Use Docker Compose for running the entire stack:
   ```bash
   docker-compose up
   ```

## Docker Support

The project uses `docker-compose.yaml` to orchestrate services. The following services are included:

- Backend
- Frontend
- Database (optional, if configured in Docker Compose)

To build and run the services:
```bash
docker-compose up --build
```

## Development Workflow

### Backend

- Use the `flask run` command for local development.
- Tests can be added to the `tests` directory and run using:
  ```bash
  pytest
  ```

### Frontend

- Use the `npm start` command for local development.
- Build the frontend for production:
  ```bash
  npm run build
  ```

### CI/CD

The Jenkins pipeline is defined in the `Jenkinsfile` located in the root of the project. Configure Jenkins to automate builds and deployments.
