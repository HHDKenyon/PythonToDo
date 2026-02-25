import sqlite3

DB_PATH = "todo_database.db"

dbconnection = None
dbcursor = None


def setup_db(path=DB_PATH):
    global dbconnection, dbcursor
    dbconnection = sqlite3.connect(path)
    dbcursor = dbconnection.cursor()
    dbcursor.execute(
        """
        CREATE TABLE IF NOT EXISTS todo_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            effort INTEGER,
            importance INTEGER,
            earliestStart DATE,
            deadline DATE,
            score REAL AS ( CAST(importance AS REAL) / effort ) STORED
        );
        """
    )
    dbconnection.commit()


def add():
    task = input("Task: ")
    effort = int(input("Effort: "))
    importance = int(input("Importance: "))
    earliestStart = input("Earliest Start (optional): ")
    deadline = input("Deadline (optional): ")
    dbcursor.execute(
        """INSERT INTO todo_items (task, effort, importance, earliestStart, deadline) VALUES (?, ?, ?, ?, ?)""",
        (task, effort, importance, earliestStart, deadline),
    )
    dbconnection.commit()


def list_items():
    dbcursor.execute("""SELECT * FROM todo_items ORDER BY score DESC""")
    items = dbcursor.fetchall()
    for item in items:
        print(item)


def edit():
    list_items()
    print(
        "Enter the new values for each field. Leave field blank to skip it without changing anything."
    )
    item_id = input("Enter the ID of the item you'd like to edit. ")

    task = input("Task: ") or None
    effort = input("Effort: ") or None
    importance = input("Importance: ") or None
    earliestStart = input("Earliest Start (optional): ") or None
    deadline = input("Deadline (optional): ") or None

    updates = []
    parameters = []

    if task is not None:
        updates.append("task = ?")
        parameters.append(task)
    if effort is not None:
        updates.append("effort = ?")
        parameters.append(effort)
    if importance is not None:
        updates.append("importance = ?")
        parameters.append(importance)
    if earliestStart is not None:
        updates.append("earliestStart = ?")
        parameters.append(earliestStart)
    if deadline is not None:
        updates.append("deadline = ?")
        parameters.append(deadline)

    if not updates:
        return

    sql = f"UPDATE todo_items SET {', '.join(updates)} WHERE id = ?"
    parameters.append(item_id)
    dbcursor.execute(sql, parameters)
    dbconnection.commit()


def rank():
    dbcursor.execute("""SELECT task FROM todo_items ORDER BY score DESC LIMIT 1""")
    item = dbcursor.fetchone()
    if item:
        print(f"The task with the highest score is: {item[0]}")
    else:
        print("No tasks found.")


def delete():
    list_items()
    item_id = input("Enter the ID of the item you'd like to delete. ")
    dbcursor.execute("""DELETE FROM todo_items WHERE id = ?""", (item_id,))
    dbconnection.commit()


def main():
    setup_db()
    while True:
        command = input(
            "What would you like to do? You can 'add', 'list', 'rank', 'edit', 'delete', or 'exit' to quit the app. "
        ).lower()
        if command == "add":
            add()
        elif command == "list":
            list_items()
        elif command == "rank":
            rank()
        elif command == "edit":
            edit()
        elif command == "delete":
            delete()
        elif command == "exit":
            break


if __name__ == "__main__":
    main()
