## NYC 311 Service Requests Web App and ETL Project

### Dataset Slice Used

This project uses a small slice of the NYC 311 Service Requests dataset as a fixture for development and testing purposes. The fixture CSV `tests/311_sample.csv` contains 5 representative records with diverse complaint types and boroughs, allowing efficient ETL ingestion and comprehensive testing without working on the full dataset.

The sample includes columns such as:

- `Unique Key`
- `Created Date`
- `Closed Date`
- `Agency`
- `Complaint Type`
- `Descriptor`
- `Borough`
- `Latitude`
- `Longitude`

***

### Project Overview

This Python Flask web application provides:

- A searchable interface filtering NYC 311 data by date range, borough, and complaint type.
- Paginated display of filtered results from MySQL.
- An aggregate view of complaints per borough.
- Automated Selenium-based end-to-end tests.
- ETL scripts to ingest data slices into MySQL.

***

### Prerequisites

- Python 3.11+
- MySQL server accessible locally or via Docker
- Google Chrome and matching ChromeDriver installed for Selenium tests

***

### Installation & Setup

1. **Install required Python packages**

```bash
pip install -r requirements.txt
```

2. **Set up MySQL database**

- Create the `nyc311` database.
- Load schema and indexes from `schema.sql`.
- Configure database credentials in `.env` file (do NOT commit your real `.env`).

Example `.env`:

```
MYSQL_HOST=localhost
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_password
MYSQL_DB=nyc311
```

***

### Running the Application

Start the Flask web application:

```bash
python app/main.py
```

Access it in a browser at `http://localhost:5000`.

***

### Running ETL

Load the fixture sample CSV into the database:

```bash
python etl/etl.py tests/fixture_sample.csv
```

Adapt `etl.py` to point to your CSV file location as needed.

***

### Running Tests

Execute Selenium end-to-end tests:

```bash
pytest -v tests/selenium_test.py
```

Ensure Chrome and matching ChromeDriver are installed and compatible.

***
