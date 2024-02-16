from bot.data_bases.psql_conn import DB_conn

class DB_order(DB_conn):

#Add user to statistic
    async def add_user_to_statistic(self, user, username, datetime):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(
                        f"INSERT INTO statistic_user (user_id, username, enter_datetime) SELECT {user}, '{username}', "
                        f"'{datetime}' WHERE NOT EXISTS (SELECT * FROM statistic_user WHERE user_id = {user});")
        except:
            print("MDA")
#Create table
    async def create_order_table(self):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute('''CREATE TABLE IF NOT EXISTS user_order (id SERIAL PRIMARY KEY,
                                                       user_id INTEGER NULL,
                                                       budget TEXT NULL,
                                                       idea TEXT NULL,
                                                       material TEXT NULL,
                                                       description TEXT NULL,
                                                       full_name TEXT NULL,
                                                       country TEXT NULL,
                                                       city TEXT NULL,
                                                       delivery TEXT NULL,
                                                       number TEXT NULL,
                                                       in_stock TEXT NULL);''')
        except:
            print("MDA")

# Adds
    async def add_user_to_db(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"INSERT INTO user_order (user_id) SELECT {user} WHERE NOT EXISTS (SELECT * FROM user_order WHERE user_id = {user});")
        except:
            print("MDA")


    async def add_budget_db(self, user, budget):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET budget='{budget}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_idea_db(self, user, idea):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET idea='{idea}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_material_db(self, user, material):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET material='{material}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_instock_db(self, user, instock):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET in_stock='{instock}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_description_db(self, user, desc):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET description='{desc}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_full_name_db(self, user, fn):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET full_name='{fn}' WHERE user_id={user};")
        except:
            print("MDA")

    async def add_country_db(self, user, country):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET country='{country}' WHERE user_id={user};")
        except:
            print("MDA")


    async def add_city_db(self, user, city):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET city='{city}' WHERE user_id={user};")
        except:
            print("MDA")


    async def add_delivery_db(self, user, delivery):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET delivery='{delivery}' WHERE user_id={user};")
        except:
            print("MDA")


    async def add_number_db(self, user, number):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(f"UPDATE user_order SET number='{number}' WHERE user_id={user};")
        except:
            print("MDA")

# Get data
    async def get_order_row(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    row = await conn.fetchrow(f"SELECT * FROM user_order WHERE user_id={user};")
        except:
            print("MDA")
        else:
            return row

# Delete row
    async def delete_user(self, user):
        try:
            if self.pool is None:
                await self.create_pool()
            async with self.pool.acquire() as conn:
                    async with conn.transaction():
                        await conn.execute(f"DELETE FROM user_order WHERE user_id = {user};")
        except:
            print("MDA")


db_order = DB_order()


