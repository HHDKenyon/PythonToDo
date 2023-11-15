import sqlite3

# Create or connect to sqlite3 database, then create cursor
dbconnection = sqlite3.connect("todo_database.db")
dbcursor = dbconnection.cursor()

# Create table in db
dbcursor.execute(
    """CREATE TABLE IF NOT EXISTS todo_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        effort INTEGER,
        importance INTEGER,
        score REAL AS ( CAST(importance AS REAL) / effort ) STORED
    )
"""
)


class ListItem:
    instances = []

    def __init__(self, task, effort, importance, score):
        self.task = task
        self.effort = effort
        self.importance = importance
        self.score = score
        ListItem.instances.append(self)

    def __str__(self):
        return f"{self.task}: {self.effort} effort and {self.importance} importance. Overall score is {self.score}."

    @classmethod
    def add(cls):
        task = input("Task: ")
        effort = int(input("Effort: "))
        importance = int(input("Importance: "))
        dbcursor.execute(
            """INSERT INTO todo_items (task, effort, importance) VALUES (?, ?, ?)""",
            (task, effort, importance),
        )
        dbconnection.commit()

    @classmethod
    def list(cls):
        dbcursor.execute("""SELECT * FROM todo_items""")
        items = dbcursor.fetchall()
        for item in items:
            print(item)

    @classmethod
    def edit(cls):
        ListItem.list()

        print(
            "Enter the new values for each field. Leave field blank to skip it without changing anything."
        )

        item_id = input("Enter the ID of the item you'd like to edit. ")

        # Ask user for new values
        task = input("Task: ") or None
        effort = input("Effort: ") or None
        importance = input("Importance: ") or None

        # Parts of the SQL statement
        updates = []
        parameters = []

        # Check which fields we need to update
        if task is not None:
            updates.append("task = ?")
            parameters.append(task)
        if effort is not None:
            updates.append("effort = ?")
            parameters.append(effort)
        if importance is not None:
            updates.append("importance = ?")
            parameters.append(importance)

        # Only proceed if there are fields to update
        if not updates:
            return

        # Construct the SQL statement
        sql = f"UPDATE todo_items SET {', '.join(updates)} WHERE id = ?"
        parameters.append(item_id)

        # Execute the update
        dbcursor.execute(sql, parameters)
        dbconnection.commit()

    @classmethod
    def delete(cls):
        ListItem.list()

        item_id = input("Enter the ID of the item you'd like to delete. ")

        dbcursor.execute("""DELETE FROM todo_items WHERE id = ?""", item_id)

    @property
    def task(self):
        return self._task

    @task.setter
    def task(self, task):
        if not task:
            raise ValueError("Missing task")
        self._task = task

    @property
    def effort(self):
        return self._effort

    @effort.setter
    def effort(self, effort):
        if not effort:
            raise ValueError("Missing effort")
        self._effort = effort

    @property
    def importance(self):
        return self._importance

    @importance.setter
    def importance(self, importance):
        if not importance:
            raise ValueError("Missing importance")
        self._importance = importance


def main():
    command = ""
    while True:
        if command == "":
            command = input(
                "What would you like to do? You can 'add', 'list', 'edit', or 'delete' tasks. "
            )
        elif command.lower() == "add":
            ListItem.add()
            command = ""
        elif command.lower() == "list":
            ListItem.list()
            command = ""
        elif command.lower() == "edit":
            ListItem.edit()
            command = ""
        elif command.lower() == "delete":
            ListItem.delete()
            command = ""
        else:
            command = ""


if __name__ == "__main__":
    main()
