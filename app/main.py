import datetime
import random
import time

from databases import Database
from fastapi import FastAPI, Request
from statsd import StatsClient

from fakes import fake_user, fake_date
from settings import DATABASE_URL, STATUS_OK, INSERT_QUERY

app = FastAPI()

db = Database(DATABASE_URL)

stats = StatsClient("telegraf", 8125, prefix="performance")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/insert")
async def insert_handler():
    await db.execute(query=INSERT_QUERY, values=fake_user())

    return STATUS_OK


@app.get("/fetch_exact")
async def fetch_exact_handler():
    query = "SELECT * FROM users WHERE birth_date = :birth_date"

    await db.execute(query=query, values={"birth_date": fake_date()})

    return STATUS_OK


@app.get("/fetch_small_range")
async def fetch_small_range_handler():
    query = "SELECT * FROM users WHERE birth_date BETWEEN :start_date AND :end_date"
    start_date = fake_date()
    end_date = start_date + datetime.timedelta(days=random.randint(1, 30))

    await db.execute(query=query, values={"start_date": start_date, "end_date": end_date})

    return STATUS_OK


@app.get("/fetch_big_range")
async def fetch_big_range_handler():
    query = "SELECT * FROM users WHERE birth_date BETWEEN :start_date AND :end_date"
    start_date = fake_date(minimum_age=18)
    end_date = start_date + datetime.timedelta(days=random.randint(1_000, 10_000))

    await db.execute(query=query, values={"start_date": start_date, "end_date": end_date})

    return STATUS_OK


@app.get("/fetch_greater_than_or_less_than")
async def fetch_greater_or_less_handler():
    if random.random() > 0.5:
        query = "SELECT * FROM users WHERE birth_date > :date"
    else:
        query = "SELECT * FROM users WHERE birth_date < :date"

    await db.execute(query=query, values={"date": fake_date()})

    return STATUS_OK


@app.get("/fetch_all")
async def fetch_all_handler():
    query = "SELECT * FROM users"

    await db.execute(query=query)

    return STATUS_OK


@app.get("/index/drop")
async def index_drop_handler(name: str):
    await db.execute(query="DROP INDEX :name ON users", values={"name": name})

    return STATUS_OK


@app.get("/index/create")
async def index_create_handler(index_type: str, name: str):
    if index_type == "hash":
        await db.execute(query="CREATE INDEX :name USING HASH ON users(birth_date)", values={"name": name})

    elif index_type == "btree":
        await db.execute(query="CREATE INDEX :name USING BTREE ON users(birth_date)", values={"name": name})

    return STATUS_OK


@app.middleware("statsd")
async def statsd_middleware(request: Request, call_next):
    start = time.monotonic_ns()

    response = await call_next(request)

    executed_time_ms = (time.monotonic_ns() - start) // 1_000_000

    action = request.url.path.strip("/").replace("/", "_")

    with stats.pipeline() as pipe:
        pipe.incr(f"request.successful.count,type= ,action={action}", 1)
        pipe.timing(f"request.successful.time,type= ,action={action}", executed_time_ms)

    response.headers["X-Process-Time"] = str(executed_time_ms)

    return response
