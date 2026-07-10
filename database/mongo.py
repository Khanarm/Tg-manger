import sqlite3

conn = sqlite3.connect("tg_manager.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

cur = conn.cursor()

# ==========================
# TABLES
# ==========================

cur.execute("""
CREATE TABLE IF NOT EXISTS userbots (
    user_id INTEGER PRIMARY KEY,
    session TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS channels (
    channel_id INTEGER PRIMARY KEY,
    title TEXT,
    username TEXT,
    userbot_id INTEGER
)
""")

conn.commit()

# ==========================
# USERBOT
# ==========================

async def save_userbot(user_id: int, session: str):
    cur.execute("""
    INSERT OR REPLACE INTO userbots
    (user_id, session)
    VALUES (?, ?)
    """, (user_id, session))
    conn.commit()


async def get_userbot(user_id: int):
    cur.execute(
        "SELECT * FROM userbots WHERE user_id=?",
        (user_id,)
    )
    row = cur.fetchone()
    return dict(row) if row else None


async def get_all_userbots():
    cur.execute("SELECT * FROM userbots")
    rows = cur.fetchall()
    return [dict(i) for i in rows]


# ==========================
# CHANNEL
# ==========================

async def save_channel(
    channel_id: int,
    title: str,
    username: str,
    userbot_id: int
):
    cur.execute("""
    INSERT OR REPLACE INTO channels
    (channel_id, title, username, userbot_id)
    VALUES (?, ?, ?, ?)
    """, (
        channel_id,
        title,
        username,
        userbot_id
    ))
    conn.commit()


async def get_channel(channel_id: int):
    cur.execute(
        "SELECT * FROM channels WHERE channel_id=?",
        (channel_id,)
    )
    row = cur.fetchone()
    return dict(row) if row else None


async def get_all_channels():
    cur.execute("SELECT * FROM channels")
    rows = cur.fetchall()
    return [dict(i) for i in rows]


async def delete_channel(channel_id: int):
    cur.execute(
        "DELETE FROM channels WHERE channel_id=?",
        (channel_id,)
    )
    conn.commit()
