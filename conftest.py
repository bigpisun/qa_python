import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    """Фикстура для BooksCollector"""
    return BooksCollector()
