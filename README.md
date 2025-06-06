# Duff Digital Product Passport

This repository contains a minimal FastAPI application that provides a simple
"digital product passport" API. Products can be registered with basic
information such as materials, manufacturing location, supply chain history, and
recycling details. The data is stored in a local SQLite database using
[SQLModel](https://sqlmodel.tiangolo.com/).

## Requirements

- Python 3.12+
- Dependencies listed in `requirements.txt`

Install them with:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
uvicorn src.app:app --reload
```

This starts the API server at `http://localhost:8000`.

Open that URL in your browser to access a simple front-end. The page lets you
add products and lists the existing ones by calling the API. It also lets you
create supplier requests and escalate them across tiers if unanswered. Each
escalation generates a new tracking URL which is shown in the request list.

## Tests

Run the tests with:

```bash
pytest
```

