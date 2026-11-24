"""Give every test its own throwaway SQLite file so tests are isolated and never touch
recipes.db (also lets parallel worktrees run tests without sharing state)."""
import pytest

import main


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test.db")
    main.init_db()
