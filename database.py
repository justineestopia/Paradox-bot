import sqlite3
import time
import random
import string

DB_PATH = 'paradox.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        discord_id TEXT PRIMARY KEY,
        key TEXT UNIQUE,
        hwid TEXT,
        expires_at INTEGER,
        executions INTEGER DEFAULT 0,
        resets INTEGER DEFAULT 0,
        banned INTEGER DEFAULT 0,
        note TEXT
    )
    ''')
    conn.commit()
    return conn, cursor

def generate_key(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_user(discord_id, key=None, expiry_days=30):
    if not key:
        key = generate_key()
    expires = int(time.time()) + expiry_days * 86400
    conn, cursor = get_db()
    cursor.execute('INSERT INTO users (discord_id, key, expires_at) VALUES (?, ?, ?)',
                   (discord_id, key, expires))
    conn.commit()
    conn.close()
    return key

def get_user(discord_id):
    conn, cursor = get_db()
    cursor.execute('SELECT * FROM users WHERE discord_id = ?', (discord_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_key(key):
    conn, cursor = get_db()
    cursor.execute('SELECT * FROM users WHERE key = ?', (key,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_hwid(discord_id, hwid):
    conn, cursor = get_db()
    cursor.execute('UPDATE users SET hwid = ? WHERE discord_id = ?', (hwid, discord_id))
    conn.commit()
    conn.close()

def add_execution(discord_id):
    conn, cursor = get_db()
    cursor.execute('UPDATE users SET executions = executions + 1 WHERE discord_id = ?', (discord_id,))
    conn.commit()
    conn.close()

def ban_user(discord_id):
    conn, cursor = get_db()
    cursor.execute('UPDATE users SET banned = 1 WHERE discord_id = ?', (discord_id,))
    conn.commit()
    conn.close()

def unban_user(discord_id):
    conn, cursor = get_db()
    cursor.execute('UPDATE users SET banned = 0 WHERE discord_id = ?', (discord_id,))
    conn.commit()
    conn.close()

def reset_hwid(discord_id):
    conn, cursor = get_db()
    cursor.execute('UPDATE users SET hwid = NULL, resets = resets + 1 WHERE discord_id = ?', (discord_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn, cursor = get_db()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(discord_id):
    conn, cursor = get_db()
    cursor.execute('DELETE FROM users WHERE discord_id = ?', (discord_id,))
    conn.commit()
    conn.close()
