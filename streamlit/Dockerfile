FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /streamlit

RUN apt-get update && \
    apt-get install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8501

COPY . .

CMD ["streamlit", "run", "ui.py"]