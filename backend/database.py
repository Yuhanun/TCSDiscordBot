import sqlite3

import aiosqlite

DATABASE_LOCATION = 'tcs_bot.db'


# Create the default structure
def create_tables():
    with sqlite3.connect(DATABASE_LOCATION) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS user "
                           "("
                           "    id          INTEGER"
                           "        CONSTRAINT user_pk"
                           "            PRIMARY KEY autoincrement,"
                           "    discord_id  INTEGER NOT NULL"
                           ");")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS user_discord_id_uindex"
                           "    ON user (discord_id);")
        connection.execute("CREATE TABLE IF NOT EXISTS karma"
                           "("
                           "    user_id     INTEGER NOT NULL"
                           "        REFERENCES user"
                           "            ON UPDATE CASCADE ON DELETE CASCADE,"
                           "    positive    INTEGER UNSIGNED NOT NULL,"
                           "    negative    INTEGER UNSIGNED NOT NULL"
                           ");")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS karma_user_id_uindex"
                           "    ON karma (user_id);")
        connection.commit()


# Get the leading karma users
async def get_top_karma(limit: int) -> [(int, int, int)]:
    async with aiosqlite.connect(DATABASE_LOCATION) as connection:
        async with connection.execute("SELECT u.discord_id, k.positive, k.negative "
                                      "FROM user u "
                                      "JOIN karma k ON u.id = k.user_id "
                                      "ORDER BY (k.positive - k.negative) DESC "
                                      "LIMIT ?;", [limit]) as cursor:
            leaders = await cursor.fetchall()
            return leaders if leaders else []


# Get the karma for a specific user
async def get_karma(discord_id: int) -> (int, int):
    async with aiosqlite.connect(DATABASE_LOCATION) as connection:
        async with connection.execute("SELECT k.positive, k.negative "
                                      "FROM user u "
                                      "JOIN karma k ON u.id = k.user_id "
                                      "WHERE u.discord_id=?;", [discord_id]) as cursor:
            karma = await cursor.fetchone()
            return karma if karma else (0, 0)


# Update the karma counts for a specific user
async def update_karma(discord_id: int, karma: (int, int)):
    async with aiosqlite.connect(DATABASE_LOCATION) as connection:
        await connection.execute("INSERT OR IGNORE INTO user (discord_id) VALUES (?);",
                                 [discord_id])
        await connection.execute("INSERT INTO karma "
                                 "(user_id, positive, negative) "
                                 "VALUES ((SELECT id FROM user WHERE discord_id=?), ?, ?) "
                                 "ON CONFLICT(user_id) DO UPDATE SET "
                                 "positive = positive + ?, "
                                 "negative = negative + ?;",
                                 [discord_id, max(karma[0], 0), max(karma[1], 0), karma[0],
                                  karma[1]])
        await connection.commit()


# Set up the defaults
create_tables()
