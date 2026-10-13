# Currency rates

## Description

This project shows simple reading currency rates from RSS source, store it to DB and expose one endpoint to present ones. Uses python,
django, sqlite and docker

It was written as a recruitment task. I gave myself a fixed amount of time for it and did as much as I could
within that time; the task brief is in `brief/`.


## Assumptions for the project

Time restriction. No more than 3 hours for coding.
The only requirement is: read RSS with currency rates, store in database and present ones in one API endpoint. In particular there are no
specification how currency rates should be accessed by API, are history of currency rates needed.

Taking into account the above assumptions, implementation is as simple as possible.

- Keep in DB only the freshest rates (no history)
- No environment stuff like Celery task, no retrying, no tests, docstrings, only reader draft contained in manage command
- Use sqlite


## TODO, what can be done better

- Keep history of currency rates
- Estimate lack of currency rates using some regression (f.e. if some days are missing)
- Wrap reading script into Celery task, allowing retrying
- Expose more useful endpoint, f.e. allowing to specify date
- Make currencies as a table based on ISO 4217, use Foreign Key in currency rates table
- Add tests, doctstring
- Use other database engine like Postgres


## Installation and test

Project provides docker-compose file to simplify start-up. It provides web container with python and django.

To startup project simple execute (you should have installed docker and docker-compose)

    :::bash
    cd currency_rates
    docker-compose up
This command start database, django application and migrate data.

Open browse and navigate to `http://localhost:8000/api/currency-rates/` to view currency rates as JSON for base currency EUR and
two target currencies with rate and date.

You can update currency rate with command

    :::bash
    docker-compose run --rm web update_currency_rate
