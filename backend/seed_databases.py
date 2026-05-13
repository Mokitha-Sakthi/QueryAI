"""
Seed Script - QueryAI Test Databases
Creates 2 MySQL databases and 2 MongoDB databases with rich sample data.

Usage (from the backend/ directory):
    python seed_databases.py

Make sure your .env has:
    MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD
    MONGODB_URI
"""

import os
import sys
import datetime
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------

def section(title):
    print("\n" + "=" * 60)
    print("  " + title)
    print("=" * 60)

def ok(msg):
    print("  [OK]  " + msg)

def warn(msg):
    print("  [WARN] " + msg)

def err(msg):
    print("  [ERR]  " + msg)

def db_label(name):
    print("\n  [DB]  " + name)

# -----------------------------------------------------------------------
# MYSQL DATABASES
# -----------------------------------------------------------------------

MYSQL_DATABASES = {

    # -- Database 1: e-commerce shop ---------------------------------------
    "queryai_shop": {
        "customers": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS customers (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    name        VARCHAR(100) NOT NULL,
                    email       VARCHAR(150) UNIQUE NOT NULL,
                    city        VARCHAR(80),
                    joined_at   DATE,
                    is_vip      BOOLEAN DEFAULT FALSE
                )
            """,
            "rows": [
                ("Alice Johnson",  "alice@example.com",  "New York",    "2022-03-15", True),
                ("Bob Smith",      "bob@example.com",    "Chicago",     "2023-01-08", False),
                ("Carol White",    "carol@example.com",  "Los Angeles", "2021-11-22", True),
                ("David Brown",    "david@example.com",  "Houston",     "2024-02-10", False),
                ("Eva Martinez",   "eva@example.com",    "Phoenix",     "2023-07-05", True),
            ],
            "insert": "INSERT IGNORE INTO customers (name, email, city, joined_at, is_vip) VALUES (%s, %s, %s, %s, %s)"
        },
        "products": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS products (
                    id          INT AUTO_INCREMENT PRIMARY KEY,
                    name        VARCHAR(150) NOT NULL,
                    category    VARCHAR(80),
                    price       DECIMAL(10,2),
                    stock       INT DEFAULT 0
                )
            """,
            "rows": [
                ("Wireless Headphones", "Electronics",  79.99, 150),
                ("Running Shoes",       "Apparel",      59.99, 200),
                ("Coffee Maker",        "Kitchen",      49.99,  80),
                ("Yoga Mat",            "Sports",       24.99, 300),
                ("Mechanical Keyboard", "Electronics", 129.99,  60),
                ("Desk Lamp",           "Office",       34.99, 120),
            ],
            "insert": "INSERT IGNORE INTO products (name, category, price, stock) VALUES (%s, %s, %s, %s)"
        },
        "orders": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS orders (
                    id            INT AUTO_INCREMENT PRIMARY KEY,
                    customer_id   INT,
                    product_id    INT,
                    quantity      INT DEFAULT 1,
                    total_price   DECIMAL(10,2),
                    status        VARCHAR(30) DEFAULT 'pending',
                    ordered_at    DATETIME,
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (product_id)  REFERENCES products(id)
                )
            """,
            "rows": [
                (1, 1, 2, 159.98, "delivered",  "2024-01-05 10:30:00"),
                (1, 5, 1, 129.99, "delivered",  "2024-02-14 14:00:00"),
                (2, 3, 1,  49.99, "shipped",    "2024-03-20 09:15:00"),
                (3, 2, 3, 179.97, "delivered",  "2024-03-25 11:45:00"),
                (4, 4, 2,  49.98, "pending",    "2024-04-01 16:00:00"),
                (5, 6, 1,  34.99, "processing", "2024-04-10 08:00:00"),
            ],
            "insert": "INSERT INTO orders (customer_id, product_id, quantity, total_price, status, ordered_at) VALUES (%s, %s, %s, %s, %s, %s)"
        },
    },

    # -- Database 2: company HR system -------------------------------------
    "queryai_hr": {
        "departments": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS departments (
                    id      INT AUTO_INCREMENT PRIMARY KEY,
                    name    VARCHAR(100) NOT NULL UNIQUE,
                    budget  DECIMAL(12,2)
                )
            """,
            "rows": [
                ("Engineering", 1500000.00),
                ("Marketing",    800000.00),
                ("Sales",       1200000.00),
                ("HR",           400000.00),
                ("Finance",      600000.00),
            ],
            "insert": "INSERT IGNORE INTO departments (name, budget) VALUES (%s, %s)"
        },
        "employees": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS employees (
                    id              INT AUTO_INCREMENT PRIMARY KEY,
                    full_name       VARCHAR(100) NOT NULL,
                    email           VARCHAR(150) UNIQUE NOT NULL,
                    department_id   INT,
                    role            VARCHAR(80),
                    salary          DECIMAL(10,2),
                    hire_date       DATE,
                    is_active       BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (department_id) REFERENCES departments(id)
                )
            """,
            "rows": [
                ("John Doe",     "john@corp.com",  1, "Senior Engineer",   95000.00, "2019-06-15", True),
                ("Jane Lee",     "jane@corp.com",  1, "Junior Engineer",   72000.00, "2022-03-01", True),
                ("Mark Evans",   "mark@corp.com",  2, "Marketing Manager", 85000.00, "2020-09-10", True),
                ("Sara Kim",     "sara@corp.com",  3, "Sales Rep",         65000.00, "2021-11-20", True),
                ("Tom Harris",   "tom@corp.com",   4, "HR Specialist",     60000.00, "2018-04-22", True),
                ("Linda Park",   "linda@corp.com", 5, "Financial Analyst", 78000.00, "2021-07-14", False),
                ("Chris Nguyen", "chris@corp.com", 1, "DevOps Engineer",   90000.00, "2020-02-28", True),
            ],
            "insert": "INSERT IGNORE INTO employees (full_name, email, department_id, role, salary, hire_date, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        },
        "leave_requests": {
            "ddl": """
                CREATE TABLE IF NOT EXISTS leave_requests (
                    id              INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id     INT,
                    leave_type      VARCHAR(50),
                    start_date      DATE,
                    end_date        DATE,
                    status          VARCHAR(20) DEFAULT 'pending',
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            """,
            "rows": [
                (1, "Annual", "2024-07-01", "2024-07-10", "approved"),
                (2, "Sick",   "2024-05-03", "2024-05-05", "approved"),
                (3, "Annual", "2024-08-15", "2024-08-22", "pending"),
                (4, "Casual", "2024-06-20", "2024-06-21", "approved"),
                (7, "Annual", "2024-09-01", "2024-09-07", "pending"),
            ],
            "insert": "INSERT INTO leave_requests (employee_id, leave_type, start_date, end_date, status) VALUES (%s, %s, %s, %s, %s)"
        },
    },
}


def seed_mysql():
    section("MySQL - Seeding Databases")
    try:
        import mysql.connector
    except ImportError:
        err("mysql-connector-python not installed. Run: pip install mysql-connector-python")
        return

    host     = os.getenv("MYSQL_HOST", "localhost")
    user     = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")

    try:
        conn = mysql.connector.connect(
            host=host, user=user, password=password, connection_timeout=5
        )
        cursor = conn.cursor()
        ok("Connected to MySQL at {} as {}".format(host, user))
    except Exception as e:
        err("Cannot connect to MySQL: {}".format(e))
        err("Make sure MySQL is running and credentials in .env are correct.")
        return

    for db_name, tables in MYSQL_DATABASES.items():
        db_label(db_name)
        cursor.execute("CREATE DATABASE IF NOT EXISTS `{}`".format(db_name))
        cursor.execute("USE `{}`".format(db_name))
        ok("Database '{}' ready".format(db_name))

        for table_name, cfg in tables.items():
            try:
                cursor.execute(cfg["ddl"])
                ok("Table '{}' created".format(table_name))
                cursor.execute("DELETE FROM `{}`".format(table_name))
                cursor.executemany(cfg["insert"], cfg["rows"])
                conn.commit()
                ok("Inserted {} rows into '{}'".format(len(cfg["rows"]), table_name))
            except Exception as e:
                warn("Table '{}': {}".format(table_name, e))
                conn.rollback()

    cursor.close()
    conn.close()
    print()
    ok("MySQL seeding complete!")
    print()
    print("  Update your .env to switch databases:")
    print('      MYSQL_DATABASE="queryai_shop"   -> e-commerce schema')
    print('      MYSQL_DATABASE="queryai_hr"     -> HR system schema')


# -----------------------------------------------------------------------
# MONGODB DATABASES
# -----------------------------------------------------------------------

MONGODB_DATABASES = {

    # -- Database 1: blog platform -----------------------------------------
    "queryai_blog": {
        "users": [
            {"name": "Alice Johnson", "email": "alice@blog.com", "role": "admin",
             "joined": datetime.datetime(2022, 1, 10), "followers": 1200, "verified": True},
            {"name": "Bob Writer",    "email": "bob@blog.com",   "role": "author",
             "joined": datetime.datetime(2023, 3, 5),  "followers": 340,  "verified": True},
            {"name": "Carol Reader",  "email": "carol@blog.com", "role": "reader",
             "joined": datetime.datetime(2024, 1, 20), "followers": 12,   "verified": False},
            {"name": "Dan Editor",    "email": "dan@blog.com",   "role": "editor",
             "joined": datetime.datetime(2021, 7, 15), "followers": 800,  "verified": True},
        ],
        "posts": [
            {"title": "Getting Started with FastAPI",
             "author": "Alice Johnson", "tags": ["python", "api", "backend"],
             "status": "published", "views": 4500, "likes": 320,
             "published_at": datetime.datetime(2024, 1, 15),
             "content": "FastAPI is a modern, fast web framework for building APIs with Python..."},
            {"title": "MongoDB for Beginners",
             "author": "Bob Writer",   "tags": ["mongodb", "nosql", "database"],
             "status": "published", "views": 3200, "likes": 215,
             "published_at": datetime.datetime(2024, 2, 8),
             "content": "MongoDB is a document-oriented NoSQL database..."},
            {"title": "React vs Vue in 2024",
             "author": "Dan Editor",   "tags": ["react", "vue", "frontend"],
             "status": "draft", "views": 0, "likes": 0,
             "published_at": None,
             "content": "Comparing the two most popular frontend frameworks..."},
            {"title": "SQL Query Optimization Tips",
             "author": "Alice Johnson", "tags": ["sql", "performance", "database"],
             "status": "published", "views": 6100, "likes": 480,
             "published_at": datetime.datetime(2024, 3, 22),
             "content": "Writing efficient SQL queries is crucial for application performance..."},
        ],
        "comments": [
            {"post_title": "Getting Started with FastAPI",
             "author": "Carol Reader", "text": "Very helpful, thanks!",
             "likes": 5, "created_at": datetime.datetime(2024, 1, 16)},
            {"post_title": "Getting Started with FastAPI",
             "author": "Bob Writer",   "text": "Great introduction to FastAPI.",
             "likes": 12, "created_at": datetime.datetime(2024, 1, 17)},
            {"post_title": "MongoDB for Beginners",
             "author": "Alice Johnson", "text": "Solid overview of MongoDB concepts.",
             "likes": 8, "created_at": datetime.datetime(2024, 2, 10)},
        ],
    },

    # -- Database 2: IoT sensor data ----------------------------------------
    "queryai_iot": {
        "devices": [
            {"device_id": "DEV-001", "name": "Temperature Sensor A", "type": "temperature",
             "location": "Warehouse 1", "firmware": "v2.1.3", "active": True,
             "registered_at": datetime.datetime(2023, 5, 12)},
            {"device_id": "DEV-002", "name": "Humidity Sensor B",    "type": "humidity",
             "location": "Greenhouse",  "firmware": "v1.8.0", "active": True,
             "registered_at": datetime.datetime(2023, 6, 1)},
            {"device_id": "DEV-003", "name": "Pressure Sensor C",    "type": "pressure",
             "location": "Warehouse 2", "firmware": "v3.0.1", "active": False,
             "registered_at": datetime.datetime(2022, 11, 20)},
            {"device_id": "DEV-004", "name": "CO2 Monitor D",        "type": "air_quality",
             "location": "Office Floor", "firmware": "v2.0.0", "active": True,
             "registered_at": datetime.datetime(2024, 1, 5)},
        ],
        "readings": [
            {"device_id": "DEV-001", "value": 22.5,  "unit": "C",   "timestamp": datetime.datetime(2024, 4, 1, 8, 0)},
            {"device_id": "DEV-001", "value": 23.1,  "unit": "C",   "timestamp": datetime.datetime(2024, 4, 1, 9, 0)},
            {"device_id": "DEV-001", "value": 24.0,  "unit": "C",   "timestamp": datetime.datetime(2024, 4, 1, 10, 0)},
            {"device_id": "DEV-002", "value": 65.3,  "unit": "RH",  "timestamp": datetime.datetime(2024, 4, 1, 8, 0)},
            {"device_id": "DEV-002", "value": 67.1,  "unit": "RH",  "timestamp": datetime.datetime(2024, 4, 1, 9, 0)},
            {"device_id": "DEV-003", "value": 1013.2,"unit": "hPa", "timestamp": datetime.datetime(2024, 4, 1, 8, 0)},
            {"device_id": "DEV-004", "value": 412.0, "unit": "ppm", "timestamp": datetime.datetime(2024, 4, 1, 8, 0)},
            {"device_id": "DEV-004", "value": 430.5, "unit": "ppm", "timestamp": datetime.datetime(2024, 4, 1, 9, 0)},
        ],
        "alerts": [
            {"device_id": "DEV-001", "level": "warning",  "message": "Temperature above 23C",
             "triggered_at": datetime.datetime(2024, 4, 1, 9, 0), "resolved": True},
            {"device_id": "DEV-004", "level": "critical", "message": "CO2 levels elevated",
             "triggered_at": datetime.datetime(2024, 4, 1, 9, 0), "resolved": False},
        ],
    },
}


def seed_mongodb():
    section("MongoDB - Seeding Databases")
    try:
        from pymongo import MongoClient
        from pymongo.errors import ServerSelectionTimeoutError
    except ImportError:
        err("pymongo not installed. Run: pip install pymongo")
        return

    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        ok("Connected to MongoDB at {}".format(uri))
    except Exception as e:
        err("Cannot connect to MongoDB: {}".format(e))
        err("Make sure MongoDB is running and MONGODB_URI in .env is correct.")
        return

    for db_name, collections in MONGODB_DATABASES.items():
        db_label(db_name)
        db = client[db_name]
        for coll_name, docs in collections.items():
            try:
                db[coll_name].drop()
                result = db[coll_name].insert_many(docs)
                ok("Collection '{}' - inserted {} documents".format(coll_name, len(result.inserted_ids)))
            except Exception as e:
                warn("Collection '{}': {}".format(coll_name, e))

    client.close()
    print()
    ok("MongoDB seeding complete!")
    print()
    print("  Update your .env to switch databases:")
    print('      MONGODB_DATABASE="queryai_blog"  -> blog platform schema')
    print('      MONGODB_DATABASE="queryai_iot"   -> IoT sensor data schema')


# -----------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print()
    print("QueryAI - Database Seeder")
    print("Populating test databases for MySQL and MongoDB")
    print()

    seed_mysql()
    seed_mongodb()

    section("Done - Summary")
    print("""
  MySQL Databases:
    queryai_shop  -> tables: customers, products, orders
    queryai_hr    -> tables: departments, employees, leave_requests

  MongoDB Databases:
    queryai_blog  -> collections: users, posts, comments
    queryai_iot   -> collections: devices, readings, alerts

  Edit MYSQL_DATABASE / MONGODB_DATABASE in backend/.env
  to point at whichever database you want to test.
    """)
