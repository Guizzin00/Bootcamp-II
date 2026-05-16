import os
import pytest
import caretrack

# Use um banco de dados de teste
TEST_DB = "test_caretrack_db.json"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: define o arquivo de banco de dados para o ambiente de teste
    caretrack.DB_FILE = TEST_DB
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    # Teardown: limpa o arquivo após os testes
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_add_task():
    assert caretrack.add_task("Beber água")
    tasks = caretrack.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Beber água"
    assert not tasks[0]["completed"]

def test_add_empty_task():
    assert not caretrack.add_task("   ")
    tasks = caretrack.load_tasks()
    assert len(tasks) == 0

def test_complete_task():
    caretrack.add_task("Alongamento")
    tasks = caretrack.load_tasks()
    task_id = tasks[0]["id"]
    
    assert caretrack.complete_task(task_id)
    tasks_updated = caretrack.load_tasks()
    assert tasks_updated[0]["completed"]

def test_remove_task():
    caretrack.add_task("Pausa para descanso")
    tasks = caretrack.load_tasks()
    task_id = tasks[0]["id"]
    
    assert caretrack.remove_task(task_id)
    assert len(caretrack.load_tasks()) == 0

def test_remove_invalid_task():
    assert not caretrack.remove_task(999)
