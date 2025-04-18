import aiosqlite

async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, handle TEXT)"
        )
        await db.commit()
