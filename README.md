# CandyDeliveryApi
REST API project for candy delivery store. Developed as entrance test for Yandex Backend School.

[![CI](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/main.yml)
[![Linting](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/Oleggr/CandyDeliveryApi/actions/workflows/linting.yml)
---

### Content

- [Quickstart](#quickstart)
- [Run tests](#run-tests)
- [What's inside](#whats-inside)
- [Routes](#routes)
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

Or using make commands:

1. Install requirements
2. Run db container with: 
```make db```
3. Run alembic migrations:
```make alembic```
4. Run app locally:
```make local```

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
│   └── schema.py    - description of db structure
└── main.py          - FastAPI application: creation and configuration
```

[Up](#candydeliveryapi)


### Routes

```
POST    /couriers                Add one or several couriers
PATCH   /couriers/{courier_id}   Update info about courier
GET     /couriers/{courier_id}   Get info about courier

POST    /orders                  Add one or several couriers
POST    /orders/assign           Assign all available orders to courier
POST    /orders/complete         Mark order as completed
```


[Up](#candydeliveryapi)


### Contacts

- Telegram - [@grit4in](https://t.me/grit4in)

[Up](#candydeliveryapi)