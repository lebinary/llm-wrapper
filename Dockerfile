FROM python:3.11 as python-base

RUN pip install --upgrade pip \ 
    && pip install "poetry==1.6.1"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi -vvv

COPY . .

RUN chmod +x scripts/run_app.sh
EXPOSE 8000

CMD ["/bin/bash", "-c", "source scripts/run_app.sh"]