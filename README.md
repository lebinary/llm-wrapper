# LLM Wrapper

## Project at a glance
This project provides a comprehensive wrapper service for Large Language Models (LLMs). While it leverages pandasAI for some core functionalities, the architecture is designed to be versatile. The framework can easily accommodate various third-party agents or serve as a foundation for building custom LLM agents from the ground up. This flexibility makes it adaptable for a wide range of LLM-based applications and use cases.
The main components of this project is in `/app` directory, which consists of:
- `/models`: stores all the classes don't link to any database (non-db models).
    - `LLMAgent`: class used to interact with third-party LLM agent.
- `/routes`: stores all the endpoints, grouped by related db model.
    - `conversation`: endpoints related to `Conversation` db model.
    - `file`: endpoints related to `File` db model.
    - `prompt`: endpoints related to `Prompt` db model.
- `/services`: stores all the helpers for endpoints, grouped by related db and non-db model
    - `conversation`: helpers related to `Conversation` db model.
    - `file`: helpers related to `File` db model.
    - `prompt`: helpers related to `Prompt` db model.
- `/templates`: stores all the templates used to generate prompts sending to the LLM.
- `db_models`: stores all db models.
- `llm_strategies`: abstract class used to store different verification/security check for different LLMs.
- `schemas`: all the schemas used in this project.
- `utils`: stores things that I don't know whereelse to store


## How to clone this project
```bash
git clone --recurse-submodules https://github.com/lebinary/llm-wrapper
```
or
```bash
git clone https://github.com/lebinary/llm-wrapper
git submodule update --init --recursive
```

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
In the terminal of your root directory, run this command:\
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
The application is available at: [http://localhost:5173](http://localhost:5173).\
You can try out the API at: [http://localhost:8000/docs](http://localhost:8000/docs).
