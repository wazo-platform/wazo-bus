FROM python:3.11-slim-bookworm
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/wazo-bus
COPY contribs/asyncapi-template.yml /app
COPY contribs/documentation.py /app

WORKDIR /app

RUN true \
    && pip install -e wazo-bus \
    && pip install pyyaml \
    && mkdir -p -m777 /app/output

ENTRYPOINT ["python", "documentation.py", "-o", "/app/output"]
