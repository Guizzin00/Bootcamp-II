import pytest
from unittest.mock import patch
import caretrack

class MockResponse:
    def __init__(self, data):
        self.data = data

class MockTable:
    def __init__(self, data_store):
        self._data_store = data_store
        self._current_op = None
        self._payload = None
        self._filters = {}
    
    def select(self, columns="*"):
        self._current_op = "select"
        return self
        
    def insert(self, payload):
        self._current_op = "insert"
        self._payload = payload
        return self
        
    def update(self, payload):
        self._current_op = "update"
        self._payload = payload
        return self
        
    def delete(self):
        self._current_op = "delete"
        return self
        
    def eq(self, column, value):
        self._filters[column] = value
        return self
        
    def order(self, column):
        return self
        
    def execute(self):
        if self._current_op == "select":
            result = self._data_store[:]
            for k, v in self._filters.items():
                result = [item for item in result if item.get(k) == v]
            return MockResponse(result)
            
        elif self._current_op == "insert":
            new_item = self._payload.copy()
            new_item['id'] = len(self._data_store) + 1
            self._data_store.append(new_item)
            return MockResponse([new_item])
            
        elif self._current_op == "update":
            updated = []
            for item in self._data_store:
                match = all(item.get(k) == v for k, v in self._filters.items())
                if match:
                    item.update(self._payload)
                    updated.append(item)
            return MockResponse(updated)
            
        elif self._current_op == "delete":
            deleted = []
            for item in self._data_store[:]:
                match = all(item.get(k) == v for k, v in self._filters.items())
                if match:
                    self._data_store.remove(item)
                    deleted.append(item)
            return MockResponse(deleted)

class MockSupabaseClient:
    def __init__(self):
        self.data_store = []
        
    def table(self, table_name):
        return MockTable(self.data_store)

@pytest.fixture
def mock_supabase():
    client = MockSupabaseClient()
    with patch("caretrack.get_supabase_client", return_value=client):
        yield client

def test_add_task(mock_supabase):
    assert caretrack.add_task("Beber água")
    tasks = caretrack.load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Beber água"
    assert not tasks[0]["completed"]

def test_add_empty_task(mock_supabase):
    assert not caretrack.add_task("   ")
    tasks = caretrack.load_tasks()
    assert len(tasks) == 0

def test_complete_task(mock_supabase):
    caretrack.add_task("Alongamento")
    tasks = caretrack.load_tasks()
    task_id = tasks[0]["id"]
    
    assert caretrack.complete_task(task_id)
    tasks_updated = caretrack.load_tasks()
    assert tasks_updated[0]["completed"]

def test_remove_task(mock_supabase):
    caretrack.add_task("Pausa para descanso")
    tasks = caretrack.load_tasks()
    task_id = tasks[0]["id"]
    
    assert caretrack.remove_task(task_id)
    assert len(caretrack.load_tasks()) == 0

def test_remove_invalid_task(mock_supabase):
    assert not caretrack.remove_task(999)
