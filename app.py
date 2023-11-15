import sqlite3

# Create or connect to sqlite3 database, then create cursor
dbconnection = sqlite3.connect('todo_database.db')
dbcursor = dbconnection.cursor()

# Create tables in db
dbcursor.execute(
    '''CREATE TABLE IF NOT EXISTS todo_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        effort INTEGER,
        importance INTEGER,
        score REAL AS ( CAST(importance AS REAL) / effort ) STORED
    )
''')

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
    def get(cls):
         task = input("Task: ")
         effort = int(input("Effort: "))
         importance = int(input("Importance: "))
         score = importance / effort
         dbcursor.execute('''INSERT INTO todo_items (task, effort, importance) VALUES (?, ?, ?)''', (task, effort, importance))
         dbconnection.commit()
    
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
         # No validation/error handling here yet.
         self._effort = effort

def addTask():
    ListItem.get()
    command = ""
    return command

def main():
    command = ""
    while True:
        if command == "":
            command = input("What would you like to do? You can 'add task' or 'show scores'. ")
        elif command.lower() == "add task":
            command = addTask()
        elif command.lower() == "show scores":
            dbcursor.execute('''SELECT * FROM todo_items''')
            items = dbcursor.fetchall()
            for item in items:
                print(item)
            #for instance in sorted(ListItem.instances, key=lambda instance: instance.score, reverse=True):
            #    print(instance.task)
            #    print(instance.effort)
            #    print(instance.importance)
            #    print(instance.score)
            command = ""
        else:
            command = ""
	
if __name__ == "__main__":
    main()