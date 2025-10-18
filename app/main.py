from flask import Flask, render_template, request
import pymysql
import math
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# MySQL configuration
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "nyc311"),
    "cursorclass": pymysql.cursors.DictCursor
}

PER_PAGE = 20  # Pagination size


def get_connection():
    return pymysql.connect(**DB_CONFIG)


@app.route("/", methods=["GET"])
def index():
    """Display 311 service requests with search filters and pagination."""
    # Filters from query args
    borough = request.args.get("borough", default="", type=str)
    complaint_type = request.args.get("complaint_type", default="", type=str)
    start_date = request.args.get("start_date", default="", type=str)
    end_date = request.args.get("end_date", default="", type=str)
    page = request.args.get("page", default=1, type=int)

    # Dynamic WHERE clause
    filters = []
    params = []
    if borough:
        filters.append("borough = %s")
        params.append(borough)
    if complaint_type:
        filters.append("complaint_type = %s")
        params.append(complaint_type)
    if start_date:
        filters.append("created_date >= %s")
        params.append(start_date)
    if end_date:
        filters.append("created_date <= %s")
        params.append(end_date)

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    # Count total records
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) AS total FROM service_requests {where_clause}", params)
        total = cur.fetchone()["total"]

    # Compute pagination
    pages = math.ceil(total / PER_PAGE)
    offset = (page - 1) * PER_PAGE

    # Fetch paginated results
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT unique_key, created_date, agency, complaint_type, borough, latitude, longitude
            FROM service_requests
            {where_clause}
            ORDER BY created_date DESC
            LIMIT %s OFFSET %s
            """,
            params + [PER_PAGE, offset]
        )
        results = cur.fetchall()
    conn.close()

    return render_template(
        "index.html",
        results=results,
        total=total,
        page=page,
        pages=pages,
        filters={"borough": borough, "complaint_type": complaint_type,
                 "start_date": start_date, "end_date": end_date}
    )


@app.route("/aggregate")
def aggregate_view():
    """Display aggregate complaints per borough."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT borough, COUNT(*) AS total_complaints
            FROM service_requests
            WHERE borough IS NOT NULL AND borough <> ''
            GROUP BY borough
            ORDER BY total_complaints DESC;
        """)
        data = cur.fetchall()
    conn.close()
    return render_template("aggregate.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)

