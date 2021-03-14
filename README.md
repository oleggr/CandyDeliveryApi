# CandyDeliveryApi
REST API project for candy delivery store. Developed as entrance test for Yandex Backend School.

[![CI](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/main.yml)
[![Linting](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/linting.yml)
---

### Content

- [Quickstart](#quickstart)
- [Run tests](#run-tests)
- [What's inside](#whats-inside)
- [Contacts](#contacts)


### Quickstart

You must have docker and docker-compose tools 
installed to run the application. 
Simply you can just run following command.

```bash
# Full project
docker-compose up -d --build
```
Also you can run parts of application separately.
It's useful for debugging.

```
# Only app container
docker-compose run -d --service-ports app

# Only database container
docker-compose run -d --service-ports db
```

[Up](#candydeliveryapi)


### Run tests

For testing used pytest library. Simply run the ```pytest``` command to run all the tests of the project.

Also tests runs automatically on each push or pull request to this repo with help of github actions.

[Up](#candydeliveryapi)


### What's inside

All web routes of the app available on /docs path.

Project structure presented below:

```
app
├── api              - web related modules
├── db               - db related modules
│   ├── migrations   - generated alembic migrations
│   └── models       - db models
│   └── schema.py    - description db structure
└── main.py          - FastAPI application creation and configuration
```

[Up](#candydeliveryapi)


### Contacts

- Telegram - [@grit4in](https://t.me/grit4in)

[Up](#candydeliveryapi)