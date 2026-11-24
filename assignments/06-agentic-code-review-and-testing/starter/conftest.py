"""Point the app at a throwaway SQLite file per test so tests never touch habits.db
and never see each other's rows."""

import pytest

import main


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test.db")
    main.init_db()
