# CURRENCY CONVERTER

## CONFIGURATION and INSTALLATION
The only requirement to run this project is `Docker` and `docker-compose`. Once you have Docker ready, follow these steps:

1. Move the provided `.env` file to the root directory. If you haven't received one, create a new `.env` file and set the following variables:

```plaintext
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CURRENCY_API_API_KEY=<YOUR-CURRENCY-API-API-KEY>
CURRENCY_CONVERTER_API_KEY=<YOUR-SERVICE-A-API-KEY> # You can generate a new one in Service A's admin panel
DB_HOST=db
DB_CLIENT_HOST=db-client
DB_PASSWORD=password
DEBUG=1
SECRET_KEY=<YOUR-SUPER-SECRET-...-SECRET-KEY>
```

2. Once the `.env` file is in place, run the containers with the following command:

```bash
docker-compose up --build
```

The necessary data will be pre-loaded from the `fixtures` directory.

## PROJECT STRUCTURE
- `app`: Contains the code for `Service A`, which is a regular Django Rest Framework API. It includes an additional `download_rates` command that facilitates gathering the latest currency exchange rates from a given date (see more: `app/converter/management/commands/download_rates.py`).
- `client`: Another Django app that represents `Service B`. In this case, it acts as a script utilizing Django solely as a DB connection layer. It communicates with `Service A` using the `requests` package.

## docker-compose services
There are seven services defined in `docker-compose`, but let's focus on the most important ones:
- `backend`: Represents the Django app for `Service A`.
- `db`: Database for `Service A`.
- `client-backend`: Represents the Django app for `Service B`.
- `db-client`: Database for `Service B`.

## Usage
#### Client
With everything up and running, you can try converting the selected currency using the following command, for example:

```bash
docker-compose run client-backend python manage.py convert_currency --amount 120 --from-currency GBP --to-currency THB --date 2023-07-13 --time 09:21
```

The response will display the result:

```plaintext
Converting 120 GBP to THB with 2023-07-13 exchange rates...
120 GBP == 5444.5455 THB [exchange rates: 2023-07-13T11:59:59Z]
```

The result will be stored in the database as the `CurrencyConversionEventLog` model, which is registered in the Django admin site (default credentials: `admin/admin`).

#### API
Alternatively, you can log in to the API's admin page (using the same credentials) to check the fetched currency exchange rates (`ExchangeRate` model) or change the settings of periodic tasks (`PERIODIC TASKS > Periodic Tasks`). The `django-celery-beat` package is used here to register all periodic tasks through the admin page, allowing for easy configuration without hardcoding in the project settings file.

To download historical rates from `CurrencyAPI`, use the following command:

```bash
docker-compose run backend python manage.py download_rates --date 2023-06-28
```

If there are no errors, the script will return the following message:

```plaintext
Downloading exchange rates from: 2023-06-28
```

For more information, feel free to contact me at <lukasz.nowak@spidermonkey.guru>.