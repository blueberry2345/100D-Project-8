class Task:
    def __init__(self, description, completed):
        self.description = description
        self.completed = completed
        self.completed_text = "No"
        self.style = "color: black;"
        self.status = "Finish"


# Function updates task object if user has completed task
    def update(self):
        if self.completed:
            self.style = "background-color: grey; color: lightgreen;"
            self.status = "Finished"
            self.completed_text = "Yes"
