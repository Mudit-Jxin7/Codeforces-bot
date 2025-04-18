import aiosqlite

async def is_verified(user_id):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute(
            "SELECT handle FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row is not None
