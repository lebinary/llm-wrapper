# LLM Wrapper

## Getting started

### Required packages

Install these required software to get started:

*   [Python](https://www.python.org/downloads/) 3.11 or above
*   [Poetry](https://poetry.eustace.io/docs/#installation)

### Set environment variables
Create an .env file in root directory with these variables
```bash
export OPENAI_API_KEY="your-api-key"
export POSTGRES_PORT="5432"
export POSTGRES_USER="postgres"
export POSTGRES_DB="postgres"
export POSTGRES_PASSWORD="password"
export DATABASE_URL="postgresql://postgres:password@db:5432/postgres"
```

### Build docker compose images and container
In the terminal of your root directory, run this command:
You might need to set these env variables first before you run
```bash
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
```

Now you can start the application
```bash
docker-compose --env-file .env up --build
```

### All done!
The application is available at: [http://localhost:5173](http://localhost:5173).
You can try out the API at: [http://localhost:8000/docs](http://localhost:8000/docs).
