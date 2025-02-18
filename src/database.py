import sqlite3
import json
import os
from typing import List
import datetime
from model import Todo

TASK__FILE = 'tasks.json'

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def load_tasks():
    if not os.path.exists(TASK__FILE):
        return []
    with open(TASK__FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []
        
def save_tasks(tasks):
    with open(TASK__FILE, 'w') as file:
        json.dump(tasks, file, indent=4)
        
def sync_db_to_json():
    tasks = get_all_todos()
    save_tasks(tasks)

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
                task TEXT,
                category TEXT,
                date_added TEXT,
                last_updated TEXT,
                date_completed TEXT,
                status INTEGER,
                position INTEGER
                )""")
    conn.commit()
    
create_table()

def insert_todo(todo: Todo):
    c.execute('Select count(*) FROM todos') 
    count = c.fetchone()[0]
    todo.position = count if count else 0
    
    with conn:
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :last_updated, :date_completed, :status, :position)',
                  {'task': todo.task, 'category': todo.category, 
                   'date_added': todo.date_added, 'last_updated': todo.last_updated,'date_completed': todo.date_completed, 
                   'status': todo.status, 'position': todo.position })
    conn.commit()
    sync_db_to_json()

def get_all_todos() ->List[Todo]:
    c.execute('Select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        task, category, date_added, last_updated, date_completed, status, position = result
        todos.append({
                'task': task,
                'category': category,
                'date_added': date_added,
                'last_updated': last_updated,
                'date_completed': date_completed,
                'status': status,
                'position': position
        })
        
    return todos    
    
def delete_todo(position: int):
    c.execute('Select count(*) from todos')
    count = c.fetchone()[0]
    
    with conn:
        c.execute('DELETE FROM todos WHERE position = :position', {'position': position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)
    conn.commit()

def change_position(old_position: int, new_position: int, commit = True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
                                            {'position_new': new_position, 'position_old': old_position})       
    if commit:
        conn.commit()
        
def update_todo(position: int, task: str = None, category: str = None, status: int = None):
    with conn:
        update_fields = []
        update_values = {'position': position, 'last_updated': datetime.datetime.now().strftime("%B %d, %Y")}
        
        if task is not None:
            update_fields.append('task = :task')
            update_values['task'] = task
        if category is not None:
            update_fields.append('category = :category')
            update_values['category'] = category
        if status is not None:
            update_fields.append('status = :status')
            update_values['status'] = status
            
        update_fields.append('last_updated = :last_updated')
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE position = :position"
        c.execute(query, update_values)
    
    conn.commit()
    sync_db_to_json()
     
def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 3, date_completed = :date_completed, last_updated = :last_updated WHERE position = :position',
                  {'date_completed': datetime.datetime.now().strftime("%B %d, %Y"), 'last_updated': datetime.datetime.now().strftime("%B %d, %Y"), 'position': position})       
    conn.commit()
    sync_db_to_json()

def reset():
    with conn:
        c.execute('DROP TABLE IF EXISTS todos')   
        conn.commit()
    create_table()
    save_tasks([])