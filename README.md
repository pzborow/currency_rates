# Currency rates

## Description

This project shows simple reading currency rates from RSS source, store it to DB and expose one endpoint to present ones. Uses python,
django, postgresql and docker


## Assumptions for the project

Time restriction. No more than 3 hours for coding.
The only requirement is: read RSS with currency rates, store in database and present ones in one API endpoint. In particular there are no
specification how currency rates should be accessed by API, are history of currency rates are needed.

Taking into account the above assumptions, implementation is as simple as possible.
- Take PLN as base currency
- Store only rates to base currency
- Keep in DB only the freshest rates (no history)


## TODO, what can be done better

- Keep history of currency rates
- Read and store more than one base currency
- Estimate lack of currency rates using some regression (f.e. if some days are missing)
- Wrap reading script into Celery task, allowing retrying
- Expose more useful endpoint, f.e. allowing specify date, pair of currencies
- Use Django Rest Framework
- Make currencies as a table based on ISO 4217, use Foreign Key in currency rates table


## Installation and test

Project provides docker-compose file to simplify start-up. It provides postgres container and web container with
python and django.

To startup project simple execute (you should have installed docker and docker-compose)

    :::bash
    cd currency_rates
    docker-compose up

This command start database, django application and migrate data.

You may also run tests

    :::bash
    docker-compose run web runtest


## Knowing issues

At first run application can't connect to database. Application container tries connect to database but database isn't started yet. Rerun
`docker-compose up` temporary solve problem.
