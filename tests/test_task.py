import pytest


from unittest.mock import patch, MagicMock
from src.todocli import app, show, add, delete, update, complete, reset_db
from src.database import get_all_todos, insert_todo, delete_todo, update_todo, complete_todo, reset

# Mocking the database functions to avoid changing the actual data
@pytest.fixture
def mock_database(mocker):
    mock_get_all_todos = mocker.patch('src.database.get_all_todos', return_value=[])
    mock_insert_todo = mocker.patch('src.database.insert_todo')
    mock_delete_todo = mocker.patch('src.database.delete_todo')
    mock_update_todo = mocker.patch('src.database.update_todo')
    mock_complete_todo = mocker.patch('src.database.complete_todo')
    mock_reset = mocker.patch('src.database.reset')

    return {
        "get_all_todos": mock_get_all_todos,
        "insert_todo": mock_insert_todo,
        "delete_todo": mock_delete_todo,
        "update_todo": mock_update_todo,
        "complete_todo": mock_complete_todo,
        "reset": mock_reset,
    }

def test_add_task(mock_database, mocker):
    mock_database["get_all_todos"].return_value = []
    
    # Using a mock to test the add functionality
    with patch('typer.echo') as mock_echo:
        add("New Task", "Study")
        mock_database["insert_todo"].assert_called_once()
        mock_echo.assert_called_with("adding New Task, Study")

def test_delete_task(mock_database, mocker):
    mock_database["get_all_todos"].return_value = [{"task": "Task 1", "category": "Study", "status": 1}]
    
    with patch('typer.echo') as mock_echo:
        delete(1)
        mock_database["delete_todo"].assert_called_once_with(0)
        mock_echo.assert_called_with("deleting 1")

def test_update_task(mock_database, mocker):
    mock_database["get_all_todos"].return_value = [{"task": "Task 1", "category": "Study", "status": 1}]
    
    with patch('typer.echo') as mock_echo:
        update(1, task="Updated Task", category="Learn", status=3)
        mock_database["update_todo"].assert_called_once_with(0, "Updated Task", "Learn", 3)
        mock_echo.assert_called_with("updating 1")

def test_complete_task(mock_database, mocker):
    mock_database["get_all_todos"].return_value = [{"task": "Task 1", "category": "Study", "status": 1}]
    
    with patch('typer.echo') as mock_echo:
        complete(1)
        mock_database["complete_todo"].assert_called_once_with(0)
        mock_echo.assert_called_with("complete 1")

def test_show_task(mock_database, mocker):
    mock_database["get_all_todos"].return_value = [
        {"task": "Task 1", "category": "Study", "status": 1, "date_added": "2025-02-18", "last_updated": "2025-02-18"}
    ]
    
    with patch('rich.console.Console.print') as mock_print:
        show()
        mock_print.assert_called()

def test_reset_db(mock_database, mocker):
    with patch('rich.console.Console.print') as mock_print:
        reset_db()
        mock_database["reset"].assert_called_once()
        mock_print.assert_called_with("[bold red]⚠️ Database Reset! All tasks deleted.[/bold red]")
