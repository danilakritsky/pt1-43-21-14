FROM python:3.10-alpine AS testing

# create directory for a new user
RUN mkdir -p /home/nonroot

# create the non-root user to run container processes
RUN addgroup -S nonroot && adduser -S -G nonroot nonroot


ENV HOME=/home/nonroot/
ENV APP_DIR=/home/nonroot/pt1-43-21-14/
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

# add poetry to path
ENV PATH "$HOME/.local/bin:$PATH"
# don't write .pyc to disk
ENV PYTHONDONTWRITEBYTECODE 1
# don't buffer stdout
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock $APP_DIR

RUN \
    # update the list of packages to get curl
    apk update \
    # add poetry dependencies
    && apk add --no-cache \
        curl \
        gcc \
        libc-dev \
        musl-dev \
        libffi-dev \
    # install poetry
    && curl -sSL https://install.python-poetry.org | python3 - \
    # don't create virtualenvs
    && poetry config virtualenvs.create false \
    && poetry install

COPY ./app $APP_DIR

# make the nonroot user the owner of the app files
RUN chown -R nonroot:nonroot $APP_DIR

USER nonroot
