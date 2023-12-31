import time
from datetime import datetime

# Define a custom function for retrying an operation with a maximum number of retries
def retry_operation(operation, max_retries=3, delay_seconds=1):
    for retry in range(max_retries):
        try:
            result = operation()
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            if retry < max_retries - 1:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
    raise Exception("Operation failed after multiple retries.")

# Memento Pattern
class TaskMemento:
    def __init__(self, task):
        self._state = task

    def get_state(self):
        return self._state

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.due_date = None
        self.priority = None
        self.tags = []

    def mark_completed(self):
        self.completed = True

    def set_due_date(self, due_date):
        self.due_date = due_date

    def set_priority(self, priority):
        self.priority = priority

    def add_tags(self, tags):
        self.tags.extend(tags)

    def remove_tags(self, tags):
        for tag in tags:
            if tag in self.tags:
                self.tags.remove(tag)

    def list_tags(self):
        return self.tags

    def get_info(self):
        status = "Completed" if self.completed else "Pending"
        info = f"{self.description} - {status}, Due: {self.due_date}, Priority: {self.priority}, Tags: {', '.join(self.tags)}"
        return info

    # Memento Pattern
    def create_memento(self):
        return TaskMemento(self)

    # Memento Pattern
    def restore_from_memento(self, memento):
        self.__dict__ = memento.get_state().__dict__

# Builder Pattern
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def with_due_date(self, due_date_str):
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        self.task.set_due_date(due_date)
        return self

    def with_priority(self, priority):
        self.task.set_priority(priority)
        return self

    def with_tags(self, tags):
        self.task.add_tags(tags)
        return self

    def build(self):
        return self.task

class ToDoListManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def mark_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.mark_completed()
                return

    def delete_task(self, task_description):
        self.tasks = [task for task in self.tasks if task.description != task_description]

    def view_tasks(self, filter_option):
        filter_option = filter_option.lower()  # Convert filter_option to lowercase for case-insensitive comparison
        if filter_option == "show all":
            return [task.get_info() for task in self.tasks]
        elif filter_option == "show completed":
            return [task.get_info() for task in self.tasks if task.completed]
        elif filter_option == "show pending":
            return [task.get_info() for task in self.tasks if not task.completed]
        else:
            return []

# User interface
def main():
    manager = ToDoListManager()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. Edit Task")
        print("5. List Tags")
        print("6. View Tasks")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD, leave empty if none): ")
            priority = input("Enter priority (High/Medium/Low, leave empty if none): ")
            tags = input("Enter tags (comma-separated, leave empty if none): ").split(',')

            task_builder = TaskBuilder(description)

            if due_date_str:
                try:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                    task_builder.with_due_date(due_date_str)  # Pass the original string, not the datetime object
                except ValueError:
                    print("Invalid due date format. Please use YYYY-MM-DD format.")

            if priority:
                task_builder.with_priority(priority)

            if tags:
                task_builder.with_tags(tags)

            # Use retry_operation to add the task with transient error handling
            task = retry_operation(lambda: task_builder.build())
            manager.add_task(task)
            print("Task added successfully!")

        elif choice == "2":
            task_description = input("Enter task description to mark as completed: ")
            manager.mark_completed(task_description)
            print(f"{task_description} marked as completed!")

        elif choice == "3":
            task_description = input("Enter task description to delete: ")
            manager.delete_task(task_description)
            print(f"{task_description} deleted!")

        elif choice == "4":
            task_description = input("Enter task description to edit: ")
            for task in manager.tasks:
                if task.description == task_description:
                    new_description = input("Enter new task description: ")
                    new_due_date = input("Enter new due date (YYYY-MM-DD, leave empty if none): ")
                    new_priority = input("Enter new priority (High/Medium/Low, leave empty if none): ")
                    new_tags = input("Enter new tags (comma-separated, leave empty if none): ").split(',')

                    task.description = new_description

                    if new_due_date:
                        try:
                            new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d")
                            task.set_due_date(new_due_date)
                        except ValueError:
                            print("Invalid due date format. Task not updated.")

                    if new_priority:
                        task.set_priority(new_priority)

                    if new_tags:
                        task.remove_tags(task.tags)  # Clear existing tags
                        task.add_tags(new_tags)

                    print("Task edited successfully!")
                    break
            else:
                print(f"No task found with description: {task_description}")

        elif choice == "5":
            task_description = input("Enter task description to list tags: ")
            for task in manager.tasks:
                if task.description == task_description:
                    tags = task.list_tags()
                    print(f"Tags for {task_description}: {', '.join(tags)}")
                    break
            else:
                print(f"No task found with description: {task_description}")

        elif choice == "6":
            filter_option = input("Enter filter option (Show all/Show completed/Show pending): ")
            tasks = manager.view_tasks(filter_option)
            if tasks:
                print("\nTasks:")
                for task in tasks:
                    print(task)
            else:
                print("No tasks found.")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
