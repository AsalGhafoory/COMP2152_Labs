def record_attempt(username, success):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO login_attempts (username, success, attempt_date) VALUES (?, ?, ?)",
        (username, success, str(datetime.datetime.now()))
    )

    conn.commit()
    conn.close()


def get_failed_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM login_attempts WHERE username = ? AND success = 0",
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def count_failures_per_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, COUNT(*) FROM login_attempts WHERE success = 0 GROUP BY username"
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_old_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM login_attempts WHERE username = ?",
        (username,)
    )

    deleted_rows = cursor.rowcount
    conn.commit()
    conn.close()

    return deleted_rows