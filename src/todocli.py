#!/usr/bin/env python
import typer
import json
import os
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, insert_todo, delete_todo, update_todo, change_position, complete_todo, reset, sync_db_to_json

TASKS_FILE = 'tasks.json'

console = Console()
app = typer.Typer()

def is_valid_position(position: int):
    tasks = get_all_todos()
    return 0 < position <= len(tasks)

@app.command(short_help='add a new item')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task,category)
    insert_todo(todo)
    show()
    
@app.command()
def delete(position: int):
    if not is_valid_position(position):
        console.print(f"[bold red]Invalid position {position}[/bold red]")
        return
     
    typer.echo(f"deleting {position}")
    delete_todo(position-1)
    show()
    
@app.command()
def update(position: int, task: str = None, category: str = None, status = None):
    if not is_valid_position(position):
        console.print(f"[bold red]Invalid position {position}[/bold red]")
        return 
    
    typer.echo(f"updating {position}")
    update_todo(position-1, task, category, status)
    show()

@app.command()
def complete(position: int):
    if not is_valid_position(position):
        console.print(f"[bold red]Invalid position {position}[/bold red]")
        return 
    
    typer.echo(f"complete {position}")
    complete_todo(position-1)
    show()
    
@app.command()
def show(listType: str = typer.Option(None, '--type', '-t', help = 'Filter by type: done, undone, in-progress')):
    tasks = get_all_todos()

    if listType == 'done':
        tasks = [task for task in tasks if task.status == 3]
    elif listType == 'undone':
        tasks = [task for task in tasks if task.status == 1]
    elif listType == 'in-progress':
        tasks = [task for task in tasks if task.status == 2]
        
    if not tasks:
        console.print("[bold red]No tasks found![/bold red]")
        return
    
    console.print("[bold magenta]Todo List[/bold magenta]!")
    table = Table(show_header=True, header_style = "bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("date_added", min_width=12, justify="right")
    table.add_column("last_updated", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    
    def get_category_color(category: str):
        COLORS = {'Learn': 'cyan', 'Youtube': 'red', 'Sport': 'cyan', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'
    for index, task in enumerate(tasks, start=1):
        c = get_category_color(task["category"])
        status = '✅' if task["status"] == 3  else '❌' if task["status"] == 1 else '🕒'
        table.add_row(str(index), task["task"], 
                      f'[{c}]{task["category"]}[/{c}]',
                      task["date_added"], 
                      task["last_updated"], 
                      status)
    console.print(table)    
    
@app.command()
def reset_db():
    console.print("[bold red]⚠️ Database Reset! All tasks deleted.[/bold red]")
    reset()    
    
    
if __name__ == "__main__":
    app()