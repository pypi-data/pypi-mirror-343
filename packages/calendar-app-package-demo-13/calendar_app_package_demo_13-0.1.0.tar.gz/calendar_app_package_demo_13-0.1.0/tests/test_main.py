import subprocess
import pytest
from calendar_app_package import main as app_main

def test_cli_add_task_and_exit(monkeypatch, capsys):
    inputs = iter([
        '1',                      # Select "Add Task"
        'Test Task',             # Title
        'Test Description',      # Description
        '04/20/2025 10:00 AM',   # Start time
        '04/20/2025 11:00 AM',   # End time
        '3'                      # Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    class MockCalendarAPI:
        def create_event(self, task):
            return "https://calendar.google.com/fake-link"

    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()
    output = capsys.readouterr().out
    assert "Task created and added to Google Calendar." in output
    assert "https://calendar.google.com/fake-link" in output

def test_cli_view_tasks_and_exit(monkeypatch, capsys):
    inputs = iter(['2', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    class MockTask:
        def __str__(self):
            return "Mock Task: 2025-04-21T10:00:00 → 2025-04-21T11:00:00"

    class MockTaskManager:
        def __init__(self):
            pass
        def list_tasks(self):
            return [MockTask()]
        def add_task(self, *args, **kwargs):
            return MockTask()

    class MockCalendarAPI:
        def create_event(self, task):
            return "https://calendar.google.com/fake-link"

    monkeypatch.setattr("calendar_app_package.main.TaskManager", MockTaskManager)
    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()

    output = capsys.readouterr().out
    assert "Task List:" in output
    assert "Mock Task" in output

def test_cli_add_task_invalid_time(monkeypatch, capsys):
    """
    ✅ Test that entering an invalid date format triggers an error message
    """
    inputs = iter([
        '1',                      # Add Task
        'Broken Task',           # Title
        'Bad date format',       # Description
        'April 30 2pm',          # Invalid start time
        'April 30 3pm',          # Invalid end time
        '3'                      # Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    class MockCalendarAPI:
        def create_event(self, task):
            return "https://calendar.google.com/fake-link"

    class MockTaskManager:
        def __init__(self): pass
        def add_task(self, *args, **kwargs):
            return MagicMock()
        def list_tasks(self):
            return []

    from calendar_app_package import main as app_main
    monkeypatch.setattr("calendar_app_package.main.TaskManager", MockTaskManager)
    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()
    output = capsys.readouterr().out

    assert "Invalid format" in output or "Failed to create task" in output

def test_cli_invalid_menu_choice(monkeypatch, capsys):
    inputs = iter(['banana', '3'])  # Invalid → Exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Mock calendar_api and task manager dependencies
    class MockCalendarAPI:
        def create_event(self, task): return "https://calendar.google.com/fake-link"

    class MockTaskManager:
        def __init__(self): pass
        def add_task(self, *args, **kwargs): return None
        def list_tasks(self): return []

    from calendar_app_package import main as app_main
    monkeypatch.setattr("calendar_app_package.main.TaskManager", MockTaskManager)
    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()
    output = capsys.readouterr().out
    assert "Invalid choice" in output


def test_cli_view_no_tasks(monkeypatch, capsys):
    inputs = iter(['2', '3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    class MockTaskManager:
        def __init__(self): pass
        def list_tasks(self): return []
        def add_task(self, *args, **kwargs): return None

    class MockCalendarAPI:
        def create_event(self, task): return "https://calendar.google.com/fake-link"

    from calendar_app_package import main as app_main
    monkeypatch.setattr("calendar_app_package.main.TaskManager", MockTaskManager)
    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()
    output = capsys.readouterr().out
    assert "No tasks added yet." in output


def test_cli_add_task_raises_general_exception(monkeypatch, capsys):
    inputs = iter([
        '1',
        'Exploding Task',
        'Something goes wrong',
        '04/30/2025 10:00 AM',
        '04/30/2025 11:00 AM',
        '3'
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    class MockCalendarAPI:
        def create_event(self, task):
            raise RuntimeError("Mock explosion")

    class MockTaskManager:
        def __init__(self): pass
        def add_task(self, *args, **kwargs):
            return MagicMock()

    from calendar_app_package import main as app_main
    monkeypatch.setattr("calendar_app_package.main.TaskManager", MockTaskManager)
    monkeypatch.setattr("calendar_app_package.main.calendar_api", MockCalendarAPI)

    app_main.main()
    output = capsys.readouterr().out
    assert "Failed to create task or calendar event" in output

# Chat GPT was used to help make mock tests for API integration.