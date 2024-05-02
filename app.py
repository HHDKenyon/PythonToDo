import sqlite3

# Create or connect to sqlite3 database, then create cursor
dbconnection = sqlite3.connect("todo_database.db")
dbcursor = dbconnection.cursor()

# Create table if it doesn't exist
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


# Need some step in here to handle the case where the table exists but needs to be modified - add or remove columns without losing data


class ListItem:
    instances = []

    def __init__(self, task, effort, importance, earliestStart=None, deadline=None, score=None):
        self.task = task
        self.effort = effort
        self.importance = importance
        self.earliestStart = earliestStart
        self.deadline = deadline
        self.score = score
        ListItem.instances.append(self)

    def __str__(self):
        return f"{self.task}: {self.effort} effort and {self.importance} importance. Overall score is {self.score}."

    @classmethod
    def add(cls):
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
        earliestStart = input("Earliest Start (optional): ") or None
        deadline = input("Deadline (optional): ") or None

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
        if earliestStart is not None:
            updates.append("earliestStart = ?")
            parameters.append(earliestStart)
        if deadline is not None:
            updates.append("deadline = ?")
            parameters.append(deadline)

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
    def rank(cls):
        dbcursor.execute("""SELECT * FROM todo_items ORDER BY score DESC LIMIT 1""")
        item = dbcursor.fetchone()
        if item:
            print(f"The task with the highest score is: {item[1]}")
        else:
            print("No tasks found.")

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
                "What would you like to do? You can 'add', 'list', 'rank', 'edit', 'delete', or 'exit' to quit the app. "
            )
        elif command.lower() == "add":
            ListItem.add()
            command = ""
        elif command.lower() == "list":
            ListItem.list()
            command = ""
        elif command.lower() == "rank":
            ListItem.rank()
            command = ""
        elif command.lower() == "edit":
            ListItem.edit()
            command = ""
        elif command.lower() == "delete":
            ListItem.delete()
            command = ""
        elif command.lower() == "exit":
            break
        else:
            command = ""

if __name__ == "__main__":
    main()
