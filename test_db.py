import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host="127.0.0.1",
        port=5432,
        user="ledgerpay",
        password="ledgerpay",
        database="ledgerpay"
    )

    print(await conn.fetchval("SELECT 1"))
    await conn.close()

asyncio.run(main())