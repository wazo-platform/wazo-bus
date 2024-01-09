FROM python:3.10-slim-bullseye
LABEL maintainer="Wazo Maintainers <dev@wazo.community>"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/xivo-bus
COPY contribs/asyncapi-template.yml /app
COPY contribs/documentation.py /app

WORKDIR /app

RUN true \
    && pip install pyyaml \
    && pip install -r xivo-bus/requirements.txt \
    && pip install -e xivo-bus \
    && mkdir -p -m777 /app/output

ENTRYPOINT ["python", "documentation.py", "-o", "/app/output"]
