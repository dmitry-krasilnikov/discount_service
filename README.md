# Local setup

## Requirements
- Python 3.10 (can be easily installed with [pyenv](https://github.com/pyenv/pyenv))
- [pipenv](https://pipenv.pypa.io/en/latest/)

## Installation
To install project dependencies run `pipenv install --dev`

## Activate virtualenv
To simplify interaction with virtualenv execute `pipenv shell`

## To set up SQLite DB and initial data
- `mkdir -p instance`
- `flask init-db`
- `flask load-data`

## Run local instance
Simply issue the command `FLASK_APP=app flask run` to run the development server

## Command examples to manually test the service
There's one brand in the DB with id=1. More cases can be found in `./tests/` directory

### Set up first discount code policy
Request: `curl -H 'Content-Type: application/json' -d $'{"amount": 10, "count": 30}' http://localhost:5000/brand/1/policy`

Response: `{"result":"success"}`

### Fetch a new code for the user
Request: `curl -H 'Content-Type: application/json' -d $'{"brandId": 1}' http://localhost:5000/user/codes`

Response: `{"code":"7D0JXVXUCKZNNHL4M25H","result":"success"}`

### Second attempt to fetch a new code fails
Request: `curl -H 'Content-Type: application/json' -d $'{"brandId": 1}' http://localhost:5000/user/codes`

Response: `{"msg":"User has already received a code","msg_id":"code_already_received","result":"error"}`

### Circumvent the restrictions!
This example shows how we can override hard-coded user_id, only for the sake of this PoC

Request: `curl -H 'Content-Type: application/json' -d $'{"brandId": 1, "userId": 2}' http://localhost:5000/user/codes`

Response: `{"code":"LUOLOS92H1WM7HNLJB3L","result":"success"}`

# Further improvements
- Implement test/debug only login endpoint to generate JWT for tests
- Implement JWT support and remove hard-coded `user_id` from `fetch_code` controller
- Validate empty requests
- Post messages to the message broker
- Re-write to FastAPI to achieve asynchronous execution and to be able to consume from message broker and update SQL storage in the same thread
- Add logging with different levels of severity > stdout so that log collection solutions could fetch them and push into shared storage
- Refactor everything! (Intentionally skipped to save time and to show TDD-in-process)
- Add static code checkers, security and complexity checkers
- Set up CI environment with static analysis and tests
- Add docker-compose with PostgreSQL database and Apache Kafka to run integration tests locally
- Set up pre-commit hooks
