From python:3.7

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade pipenv

ENV APP_HOME /app
WORKDIR $APP_HOME
EXPOSE 80

CMD ["bin/run"]

COPY Pipfile Pipfile.lock $APP_HOME/

RUN pipenv install --dev

COPY . $APP_HOME/
