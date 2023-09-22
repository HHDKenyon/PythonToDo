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
         return cls(task, effort, importance, score)
    
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
            command = input("What would you like to do? You can 'add task', 'show scores', or 'exit'. ")
        elif command.lower() == "add task":
            command = addTask()
        elif command.lower() == "show scores":
            for instance in ListItem.instances:
                print(instance.task)
                print(instance.effort)
                print(instance.importance)
                print(instance.score)
            command = ""
        elif command.lower == "exit":
            exit()
        else:
            command = ""
	
if __name__ == "__main__":
    main()