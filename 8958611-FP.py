# Schedule maker.
# This program creates a schedule to complete tasks.
# Author: Krish Dumaswala
# Date: August 07, 2024


class Task:
    def __init__(self, name, timeRequired, priority, dueDate, targetDate):
        # Add a task's name, time requirement, priority, due date, and desired date at the beginning.
        self.name = name
        self.timeRequired = timeRequired
        self.priority = priority
        self.dueDate = dueDate
        self.targetDate = targetDate


def getTasks():
    # function that collects user tasks
    tasks = []
    while True:
        try:
            # Ask the user how many tasks they have
            numberOfTasks = int(input("Enter the number of tasks: "))
            if numberOfTasks < 1:
                raise ValueError("Number of tasks should be at least 1.")
            break
        except ValueError:
            print("Please enter a valid number of tasks.")

    for i in range(1, numberOfTasks + 1):
        print(f"\nTask {i}:")

        # Ask task name
        while True:
            name = input("Enter task name: ")
            if name.strip():
                break
            else:
                print("Please enter a valid task name.")

        # Ask time required for the task
        while True:
            try:
                timeRequired = float(input("Enter required time(hours): "))
                if timeRequired <= 0:
                    raise ValueError("Required time should be greater than zero.")
                break
            except ValueError:
                print("Please enter a valid required time.")

        # Ask priority level for the task
        while True:
            try:
                priority = int(input("Enter priority (1-5, 1 being highest): "))
                if priority < 1 or priority > 5:
                    raise ValueError("Priority should be between 1 and 5.")
                break
            except ValueError:
                print("Please enter a valid priority.")

        # Ask due date of the task
        while True:
            dueDate = input("Enter due date (DD-MM-YYYY HH:MM AM/PM): ")
            try:
                dueDateParts = dueDate.split(" ")
                datePart = dueDateParts[0].split("-")
                timePart = dueDateParts[1].split(":")
                amPm = dueDateParts[2]
                if len(datePart) != 3 or len(timePart) != 2 or amPm not in ["AM", "PM"]:
                    raise ValueError
                day, month, year = (
                    int(datePart[0]),
                    int(datePart[1]),
                    int(datePart[2]),
                )
                hour, minute = int(timePart[0]), int(timePart[1])
                if hour < 1 or hour > 12 or minute < 0 or minute > 59:
                    raise ValueError
                break
            except ValueError:
                print(
                    "Please enter a valid due date in the format DD-MM-YYYY HH:MM AM/PM."
                )

        # Ask completion date for the task
        while True:
            targetDate = input("Enter desired completion day (DD-MM-YYYY): ")
            try:
                datePart = targetDate.split("-")
                if len(datePart) != 3:
                    raise ValueError
                day, month, year = (
                    int(datePart[0]),
                    int(datePart[1]),
                    int(datePart[2]),
                )
                break
            except ValueError:
                print("Please enter a valid completion day in the format DD-MM-YYYY.")

        # Create and add the task to the list
        tasks.append(Task(name, timeRequired, priority, dueDate, targetDate))
    return tasks


def prioritizeTasks(tasks):
    # Function to sort tasks by priority and due date
    for i in range(len(tasks)):
        for j in range(i + 1, len(tasks)):
            if (tasks[i].priority > tasks[j].priority) or (
                tasks[i].priority == tasks[j].priority
                and tasks[i].dueDate > tasks[j].dueDate
            ):
                # If a task's priority or due date is the same, switch them.
                tasks[i], tasks[j] = tasks[j], tasks[i]


def scheduleTasks(tasks):
    # Function to arrange the tasks in a schedule
    prioritizeTasks(tasks)

    startHour = 10  # Start work day at 10 AM
    endHour = 22  # End work day at 10 PM

    schedule = []
    currentDay = None

    for i in tasks:
        targetDate = i.targetDate

        if targetDate != currentDay:
            startHour = 10  # Reset start hour if the day changes
            currentDay = targetDate

        workingHours = endHour - startHour

        if i.timeRequired <= workingHours:
            startTime = startHour
            endTime = startHour + i.timeRequired
            schedule.append((i.name, targetDate, startTime, endTime))
            startHour += i.timeRequired

            if targetDate == currentDay and startHour >= 12:
                startHour += 0.5  # Add a break if needed
        else:
            print(
                f"Task '{i.name}' cannot be scheduled within the workday on {targetDate}."
            )

    return schedule


def printSchedule(schedule):
    # Function to print and save the schedule to a file
    with open("tasks_schedule.txt", "w") as file:
        for taskName, day, start, end in schedule:
            startPeriod = "AM" if start < 12 else "PM"
            endPeriod = "AM" if end < 12 else "PM"

            startDisplay = start if start <= 12 else start - 12
            endDisplay = end if end <= 12 else end - 12

            startHour = int(startDisplay) if int(startDisplay) != 0 else 12
            endHour = int(endDisplay) if int(endDisplay) != 0 else 12

            output = (
                f"\nTask '{taskName}' on {day} from {startHour}:"
                f"{int((start - int(start)) * 60):02d} {startPeriod} to {endHour}:"
                f"{int((end - int(end)) * 60):02d} {endPeriod}"
            )

            print(output)
            file.write(output + "\n")


# main program starts here
tasks = getTasks()
schedule = scheduleTasks(tasks)
printSchedule(schedule)