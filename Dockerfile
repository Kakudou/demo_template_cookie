FROM python:3.12-alpine AS base
ENV CONNECTOR_TYPE=EXTERNAL_IMPORT

# Install Python modules
# hadolint ignore=DL3003
RUN apk update && apk upgrade && \
    apk --no-cache add git build-base libmagic libffi-dev libxml2-dev libxslt-dev && \
    pip3 install --no-cache-dir --upgrade pip


FROM base AS package
# Copy the package
COPY DemoTemp /opt/template_connector/demo_temp
COPY pyproject.toml /opt/pyproject.toml

RUN cd /opt/ && \
    pip3 install --no-cache-dir . && \
    apk del git build-base && \
    rm /opt/pyproject.toml && \
    rm -rf /opt/demo_temp

FROM package AS app
# Run the app
CMD ["DemoTemp"]
