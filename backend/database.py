import sqlite3

import discord

import main


def create_tables():
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user "
                   "("
                   "    id          INTEGER"
                   "        CONSTRAINT user_pk"
                   "            PRIMARY KEY autoincrement,"
                   "    discord_id  INTEGER NOT NULL"
                   ");")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS user_discord_id_uindex"
                   "    ON user (discord_id);")
    cursor.execute("CREATE TABLE IF NOT EXISTS karma"
                   "("
                   "    user_id     INTEGER NOT NULL"
                   "        REFERENCES user"
                   "            ON UPDATE CASCADE ON DELETE CASCADE,"
                   "    positive    INTEGER UNSIGNED NOT NULL,"
                   "    negative    INTEGER UNSIGNED NOT NULL"
                   ");")
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS karma_user_id_uindex"
                   "    ON karma (user_id);")

    connection.commit()
    cursor.close()


def get_top_karma(limit: int) -> [(int, (int, int))]:
    cursor = connection.cursor()
    cursor.execute("SELECT k.positive, k.negative, u.discord_id "
                   "FROM user u "
                   "JOIN karma k ON u.id = k.user_id "
                   "LIMIT ?;", [limit])

    leaders = cursor.fetchall()
    cursor.close()
    return leaders if leaders else []


def get_karma(discord_id: int) -> (int, int):
    cursor = connection.cursor()
    cursor.execute("SELECT k.positive, k.negative "
                   "FROM user u "
                   "JOIN karma k ON u.id = k.user_id "
                   "WHERE u.discord_id=?;", [discord_id])
    karma = cursor.fetchone()
    cursor.close()
    return karma if karma else (0, 0)


async def set_karma(discord_id: int, karma: (int, int)):
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO user (discord_id) VALUES (?);", [discord_id])
    cursor.execute("INSERT INTO karma "
                   "(user_id, positive, negative) "
                   "VALUES ((SELECT id FROM user WHERE discord_id=?), ?, ?) "
                   "ON CONFLICT(user_id) DO UPDATE SET "
                   "positive=?, negative=?;",
                   [discord_id, karma[0], karma[1], karma[0], karma[1]])

    connection.commit()
    cursor.close()


async def update_karma(discord_id: int, karma: (int, int)):
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO user (discord_id) VALUES (?);", [discord_id])
    cursor.execute("INSERT INTO karma "
                   "(user_id, positive, negative) "
                   "VALUES ((SELECT id FROM user WHERE discord_id=?), ?, ?) "
                   "ON CONFLICT(user_id) DO UPDATE SET "
                   "positive = positive + ?, "
                   "negative = negative + ?;",
                   [discord_id, max(karma[0], 0), max(karma[1], 0), karma[0], karma[1]])

    connection.commit()
    cursor.close()


connection = sqlite3.connect('tcs_bot.db')
create_tables()
