import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        user="ledgerpay",
        password="ledgerpay",
        database="ledgerpay",
        host="127.0.0.1",
        port=5432
    )

    print("Connected successfully!")
    print(await conn.fetchval("SELECT 1"))
    await conn.close()

asyncio.run(main())
