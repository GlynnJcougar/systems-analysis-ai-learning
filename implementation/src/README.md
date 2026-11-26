# Application Foundation

This directory contains the Django project foundation. It does not yet
implement event features, Supabase Auth, or administrator setup. Deployment
security configuration is also incomplete; this foundation is not
production-ready.

## Setup on Windows

Install Python 3.14 and have a PostgreSQL database available. From the
repository root in PowerShell:

```powershell
Set-Location implementation
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
```

Set a persistent, private Django secret key and a PostgreSQL connection URL
in the environment. The URL must identify an existing database; encode special
characters in credentials as URL components. For hosted databases, configure
TLS as required by the provider. Do not commit credentials.

```powershell
$env:DJANGO_SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
$env:DATABASE_URL = 'postgresql://<user>:<password>@<host>:5432/<database>?sslmode=require'
```

The generated key above is for the current shell; retain a securely generated
key in your deployment's secret configuration across restarts. Django debug
mode is off by default. For local development only, set
`$env:DJANGO_DEBUG = 'true'`. `DJANGO_ALLOWED_HOSTS` is a comma-separated
list, defaulting to localhost addresses.

## Initialize and run

From `implementation` with the environment configured:

```powershell
python src\manage.py migrate
python src\manage.py check
python src\manage.py runserver
```

`migrate` initializes Django's infrastructure tables in the configured
database; it does not create the PostgreSQL database itself or application
business tables. The root page is only a startup placeholder.

## Build

```powershell
python -m build --wheel
```

The wheel is placed in `implementation\dist`.

## Tests

```powershell
python src\manage.py test tests
```

Tests use PostgreSQL and create and delete a separate test database. Use a
dedicated development database account with permission to create test
databases, not a production database. No Supabase credentials are needed
for this foundation.
