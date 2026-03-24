def add_credential(website, username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )

    conn.commit()
    conn.close()


def get_all_credentials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM vault ORDER BY website ASC"
    )

    results = cursor.fetchall()
    conn.close()
    return results


def find_credential(website):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM vault WHERE website = ?",
        (website,)
    )

    results = cursor.fetchall()
    conn.close()
    return results