import datetime

class Todo:
    def __init__(self, task, category,
                 date_added=None, date_completed=None, last_updated=None,
                 status=None, position=None):
        self.task = task
        self.category = category
        self.date_added = date_added if date_added is not None else datetime.datetime.now().strftime("%B %d, %Y")
        self.date_completed =  date_completed if date_completed is not None else None
        self.last_updated = last_updated if last_updated is not None else datetime.datetime.now().strftime("%B %d, %Y")
        self.status = status if status is not None else 1 # 1 for incomplete, 2 for in-progress, 3 for completed
        self.position = position if position is not None else None # Ordering of tasks
        
    def __repr__(self):
        return f"({self.task}, {self.category}, {self.date_added}, {self.last_updated}, {self.date_completed}, {self.status}, {self.position})"