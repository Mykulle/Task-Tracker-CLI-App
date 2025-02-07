import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, insert_todo, delete_todo, update_todo, change_position, complete_todo, reset

console = Console()

app = typer.Typer()

@app.command(short_help='add a new item')
def add(task: str, category: str):
    typer.echo(f"adding {task}, {category}")
    todo = Todo(task,category)
    insert_todo(todo)
    show()
    
@app.command()
def delete(position: int):
    typer.echo(f"deleting {position}")
    delete_todo(position-1)
    show()
    
@app.command()
def update(position: int, task: str = None, category: str = None, status = None):
    typer.echo(f"updating {position}")
    update_todo(position-1, task, category, status)
    show()

@app.command()
def complete(position: int):
    typer.echo(f"complete {position}")
    complete_todo(position-1)
    show()
    
@app.command()
def show(ListType: str = None):
    tasks = get_all_todos()
    
    if ListType == 'done':
        tasks = [task for task in tasks if task.status == 3]
    elif ListType == 'undone':
        tasks = [task for task in tasks if task.status == 1]
    elif ListType == 'in-progress':
        tasks = [task for task in tasks if task.status == 2]
        
    console.print("[bold magenta]Todo List[/bold magenta]!")
    table = Table(show_header=True, header_style = "bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    
    def get_category_color(category: str):
        COLORS = {'Learn': 'cyan', 'Youtube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'
    for index, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        status = '✅' if task.status == 3  else '❌' if task.status == 1 else '🕒'
        table.add_row(str(index), task.task, f'[{c}]{task.category}[/{c}]', status)
    console.print(table)    
    
@app.command()
def reset_db():
    reset()
    typer.echo("[bold red]Database Reset! All tasks deleted.[/bold red]")

if __name__ == "__main__":
    app()