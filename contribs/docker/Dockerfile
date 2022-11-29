FROM python:3.7-slim-buster
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN true \
    && mkdir -p /app/output \
    && install -dm777 /app/output \
    && pip install --upgrade pip pyyaml 'importlib-metadata<5' kombu six \
        https://github.com/wazo-platform/xivo-bus/archive/master.zip

COPY asyncapi-template.yml /app
COPY documentation.py /app

WORKDIR /app
ENTRYPOINT ["python", "documentation.py", "-o", "/app/output"]
