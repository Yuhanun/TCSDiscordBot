import sqlite3
import aiosqlite
import inspect

# print(self.bot._db)

from backend.config import DATABASE_LOCATION


class Settings:
    CURRENT_VERSION = 1

    def __init__(self, version: int = CURRENT_VERSION,
                 das_mooi_threshold: int = 5,
                 das_mooi_channel: int = 637237240766136331,
                 das_niet_mooi_channel: int = 637237272864882688):
        self._version = version
        self._das_mooi_threshold = das_mooi_threshold
        self._das_mooi_channel = das_mooi_channel
        self._das_niet_mooi_channel = das_niet_mooi_channel

    def get_version(self) -> int:
        return self._version

    def get_das_mooi_threshold(self) -> int:
        return self._das_mooi_threshold

    def get_das_mooi_channel(self) -> int:
        return self._das_mooi_channel

    def get_das_niet_mooi_channel(self) -> int:
        return self._das_niet_mooi_channel

    async def set_das_mooi_threshold(self, das_mooi_threshold: int) -> None:
        self._das_mooi_threshold = das_mooi_threshold
        await _update_settings(self)

    async def set_das_mooi_channel(self, das_mooi_channel: int) -> None:
        self._das_mooi_channel = das_mooi_channel
        await _update_settings(self)

    async def set_das_niet_mooi_channel(self, das_niet_mooi_channel: int) -> None:
        self._das_niet_mooi_channel = das_niet_mooi_channel
        await _update_settings(self)


# Create the default structure
def create_tables() -> Settings:
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
        connection.execute("CREATE TABLE IF NOT EXISTS forwarded_messages"
                           "("
                           "    message_id INTEGER UNSIGNED NOT NULL,"
                           "    positive BOOLEAN NOT NULL,"
                           "    CONSTRAINT forwarded_message_pk"
                           "        UNIQUE (message_id, positive)"
                           ");")
        connection.execute("CREATE TABLE IF NOT EXISTS laf_counter"
                           "("
                           "    user_id INTEGER UNSIGNED NOT NULL UNIQUE"
                           "        REFERENCES user"
                           "            ON UPDATE CASCADE ON DELETE CASCADE,"
                           "    count   INTEGER UNSIGNED NOT NULL"
                           ");")
        # I know, this is a very bad idea, but John forced me to do this
        connection.execute("CREATE TABLE IF NOT EXISTS setting"
                           "("
                           "    version                 INTEGER UNSIGNED NOT NULL,"
                           "    das_mooi_threshold      INTEGER UNSIGNED NOT NULL,"
                           "    das_mooi_channel        INTEGER UNSIGNED NOT NULL,"
                           "    das_niet_mooi_channel   INTEGER UNSIGNED NOT NULL"
                           ");")
        connection.commit()

        cursor = connection.cursor()
        cursor.execute("SELECT version, das_mooi_threshold, "
                       "das_mooi_channel, das_niet_mooi_channel "
                       "FROM setting")
        settings = cursor.fetchone()
        cursor.close()
        if not settings:
            settings = Settings()
            connection.execute("INSERT INTO setting "
                               "(version, das_mooi_threshold, "
                               "das_mooi_channel, das_niet_mooi_channel) "
                               "VALUES (?, ?, ?, ?)", (settings.get_version(),
                                                       settings.get_das_mooi_threshold(),
                                                       settings.get_das_mooi_channel(),
                                                       settings.get_das_niet_mooi_channel()))
            return settings
        else:
            return Settings(settings[0], settings[1], settings[2], settings[3])


# Update the settings in the database
async def _update_settings(self) -> None:
  connection = self.bot._db
  await connection.execute("UPDATE setting SET "
                           "das_mooi_threshold=?, "
                           "das_mooi_channel=?, "
                           "das_niet_mooi_channel=?;", (settings.get_das_mooi_threshold(),
                                                        settings.get_das_mooi_channel(),
                                                        settings.get_das_niet_mooi_channel()))
  await connection.commit()


# Get the leading karma users
async def get_top_karma(self, limit: int) -> [(int, int, int)]:
  connection = self.bot._db
  cursor = await connection.execute("SELECT u.discord_id, k.positive, k.negative "
                                    "FROM user u "
                                    "JOIN karma k ON u.id = k.user_id "
                                    "WHERE k.positive <> 0 OR k.negative <> 0 "
                                    "ORDER BY (k.positive - k.negative) DESC "
                                    "LIMIT ?;", [limit])
  leaders = await cursor.fetchall()
  await cursor.close()
  return leaders if leaders else []


# Get the leading negative karma users
async def get_reversed_top_karma(self, limit: int) -> [(int, int, int)]:
  connection = self.bot._db
  cursor = await connection.execute("SELECT u.discord_id, k.positive, k.negative "
                                      "FROM user u "
                                      "JOIN karma k ON u.id = k.user_id "
                                      "WHERE k.positive <> 0 OR k.negative <> 0 "
                                      "ORDER BY (k.positive - k.negative) ASC "
                                      "LIMIT ?;", [limit])
  leaders = await cursor.fetchall()
  await cursor.close()
  return leaders if leaders else []


# Get the karma for a specific user
async def get_karma(self, discord_id: int) -> (int, int):
  connection = self.bot._db
  cursor = await connection.execute("SELECT k.positive, k.negative "
                                    "FROM user u "
                                    "JOIN karma k ON u.id = k.user_id "
                                    "WHERE u.discord_id=?;", [discord_id])
  karma = await cursor.fetchone()
  return karma if karma else (0, 0)


# Update the karma counts for a specific user
async def update_karma(self, discord_id: int, karma: (int, int)) -> None:
  connection = self.bot._db
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


# Get the most laffe users
async def get_top_laf(self, limit: int) -> [(int, int)]:
  connection = self.bot._db
  cursor = await connection.execute("SELECT u.discord_id, l.count "
                                    "FROM user u "
                                    "JOIN laf_counter l ON u.id = l.user_id "
                                    "ORDER BY (l.count) DESC "
                                    "LIMIT ?;", [limit])
  leaders = await cursor.fetchall()
  await cursor.close()
  return leaders if leaders else []


# Get the least laffe users
async def get_reversed_top_laf(self, limit: int) -> [(int, int)]:
  connection = self.bot._db
  cursor = await connection.execute("SELECT u.discord_id, l.count "
                                      "FROM user u "
                                      "JOIN laf_counter l ON u.id = l.user_id "
                                      "ORDER BY (l.count) ASC "
                                      "LIMIT ?;", [limit])
  leaders = await cursor.fetchall()
  await cursor.close()
  return leaders if leaders else []


# Get the laf_counter for a specific user
async def get_laf(self, discord_id: int) -> int:
  connection = self.bot._db
  cursor = await connection.execute("SELECT l.count "
                                "FROM user u "
                                "JOIN laf_counter l ON u.id = l.user_id "
                                "WHERE u.discord_id=?;", [discord_id])
  laf_counter = await cursor.fetchone()
  await cursor.close()
  return laf_counter[0] if laf_counter else 0

# Update the laf_counter for a specific user
async def update_laf(self, discord_id: int, count: int) -> None:
  connection = self.bot._db
  await connection.execute("INSERT OR IGNORE INTO user (discord_id) VALUES (?);",
                           [discord_id])
  await connection.execute("INSERT INTO laf_counter "
                           "(user_id, count) "
                           "VALUES ((SELECT id FROM user WHERE discord_id=?), ?) "
                           "ON CONFLICT(user_id) DO UPDATE SET "
                           "count = count + ?; ",
                           [discord_id, max(count, 0), count ])
  await connection.commit()


async def is_forwarded(self, message_id: int, positive: bool) -> bool:
  connection = self.bot._db
  cursor = await connection.execute("SELECT message_id "
                                      "FROM forwarded_messages "
                                      "WHERE message_id=? AND positive=?;",
                                      (message_id, positive))
  result = await cursor.fetchone()
  await cursor.close()
  return result is not None


async def add_forwarded_message(self, message_id: int, positive: bool) -> None:
  connection = self.bot._db
  await connection.execute("INSERT INTO forwarded_messages "
                         "(message_id, positive) "
                         "VALUES (?, ?);", (message_id, positive))
  await connection.commit()


# Set up the defaults
settings = create_tables()
