from bot.data_bases.psql_conn import DB_conn

class DB_instock(DB_conn):
    async def get_data10(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch("SELECT * FROM instock_photo WHERE photo1 != '' OR image_id1 "
                                            "IS NOT NULL ORDER BY id LIMIT 10;")
        except:
            print('MDA')
        else:
            return rows


    async def get_data_more(self, offset):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    rows = await conn.fetch(f"SELECT * FROM instock_photo WHERE photo1 != '' OR image_id1 "
                                            f"IS NOT NULL ORDER BY id LIMIT 10 OFFSET {offset};")
        except:
            print('MDA')
        else:
            return rows

    async def get_specific_row(self, item_id):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM instock_photo WHERE id={item_id};")
        except:
            print('MDA')
        else:
            return row

    async def get_rows_count(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    data = await conn.execute(f"SELECT count(*) FROM instock_photo;")
                    rows = await conn.fetchrow(data)
                    rows_count = rows[0]
        except:
            print('MDA')
        else:
            return rows_count

    async def add_image_id(self, item_id, image_id, name_image_id, num):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE instock_photo SET image_id{num}='{image_id}', "
                                       f"name_image_id{num}='{name_image_id}' WHERE id='{item_id}';")
        except:
            print("MDA")

db_instock = DB_instock()