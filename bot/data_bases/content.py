from bot.data_bases.psql_conn import DB_conn

class DB_content(DB_conn):
    async def get_feedback10(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch("SELECT * FROM contentadm_feedback ORDER BY id LIMIT 10;")
        except:
            print('MDA')
        else:
            return rows

    async def get_feedback_more(self, offset):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM contentadm_feedback ORDER BY id LIMIT 10 OFFSET {offset};")
        except:
            print('MDA')
        else:
            return rows

    async def add_image_id(self, rev_id, image_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE contentadm_feedback SET image_id='{image_id}' WHERE id={rev_id};")
        except:
            print("MDA")

db_content = DB_content()