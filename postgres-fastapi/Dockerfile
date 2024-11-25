FROM unit:1.33.0-python3.11
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
COPY . /postgres-fastapi
WORKDIR /postgres-fastapi
RUN pip install uv fastapi uvicorn
RUN uv pip install -r pyproject.toml --system 
EXPOSE 8000 5432

COPY config.json /docker-entrypoint.d/
