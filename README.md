# market-values-api
One web api to query market value for listed companies, which is used to illustrate the use of [AsyncIO](https://docs.python.org/3/library/asyncio.html), [aiohttp](https://aiohttp.readthedocs.io/en/stable/), as well as unit tests with [asynctest](https://asynctest.readthedocs.io/en/latest/).

## Setup project

Install [Docker](https://docs.docker.com/install/) & [Docker Compose](https://docs.docker.com/compose/install/)

Then,

```
docker-compose build
```

## Run unit tests

```
docker-compose up test
```

## Run the web server

```
docker-compose up web
```

## Run the development container

```
docker-compose run --rm dev
```
