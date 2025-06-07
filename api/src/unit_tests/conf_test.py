import pytest

@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASS", "1")
    monkeypatch.setenv("DB_NAME", "postgres")
