import asyncio

from fakes import fake_user
from main import db
from settings import INSERT_QUERY, TOTAL_USERS


def generate_values(n):
    return [fake_user() for _ in range(n)]
    # res = []
    # for _ in range(n):
    #     res.append(fake_user())
    #
    #     await asyncio.sleep(0)  # giving control back to event loop
    #
    # return res


async def insert_batch(n):
    values = generate_values(n)
    await db.execute_many(query=INSERT_QUERY, values=values)


async def main():
    print("Connection to database...")
    await db.connect()
    print("Seeding database...")

    total = TOTAL_USERS
    in_batch = 1_000
    tasks_limit = 10

    for i in range(total // in_batch // tasks_limit):
        tasks = [insert_batch(in_batch) for _ in range(tasks_limit)]

        await asyncio.gather(*tasks)

        print(f"\rInserted {(i + 1) * tasks_limit * in_batch} out of {total}", end="")

    print("Seeding database completed...")


if __name__ == "__main__":
    asyncio.run(main())
