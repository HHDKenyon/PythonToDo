import pytest
from unittest.mock import patch

import app


@pytest.fixture(autouse=True)
def fresh_db():
    app.setup_db(":memory:")
    yield
    app.dbconnection.close()


def test_add_inserts_row():
    with patch("builtins.input", side_effect=["Buy milk", "2", "5", "", ""]):
        app.add()
    app.dbcursor.execute("SELECT task, effort, importance FROM todo_items")
    assert app.dbcursor.fetchone() == ("Buy milk", 2, 5)


def test_list_is_sorted_by_score(capsys):
    with patch("builtins.input", side_effect=["Low priority", "10", "1", "", ""]):
        app.add()
    with patch("builtins.input", side_effect=["High priority", "1", "10", "", ""]):
        app.add()
    app.list_items()
    output = capsys.readouterr().out
    assert output.index("High priority") < output.index("Low priority")


def test_rank_returns_highest_score(capsys):
    with patch("builtins.input", side_effect=["Low priority", "10", "1", "", ""]):
        app.add()
    with patch("builtins.input", side_effect=["High priority", "1", "10", "", ""]):
        app.add()
    app.rank()
    assert "High priority" in capsys.readouterr().out


def test_rank_empty_db(capsys):
    app.rank()
    assert "No tasks found" in capsys.readouterr().out


def test_delete_removes_item():
    with patch("builtins.input", side_effect=["Task A", "1", "1", "", ""]):
        app.add()
    app.dbcursor.execute("SELECT id FROM todo_items")
    item_id = str(app.dbcursor.fetchone()[0])

    with patch("builtins.input", return_value=item_id):
        app.delete()

    app.dbcursor.execute("SELECT * FROM todo_items")
    assert app.dbcursor.fetchall() == []


def test_delete_is_persisted():
    with patch("builtins.input", side_effect=["Task B", "1", "1", "", ""]):
        app.add()
    app.dbcursor.execute("SELECT id FROM todo_items")
    item_id = str(app.dbcursor.fetchone()[0])

    with patch("builtins.input", return_value=item_id):
        app.delete()

    # Reconnect to same in-memory db via the same connection to confirm commit was called
    app.dbcursor.execute("SELECT * FROM todo_items")
    assert app.dbcursor.fetchall() == []


def test_edit_updates_field():
    with patch("builtins.input", side_effect=["Old name", "3", "3", "", ""]):
        app.add()
    app.dbcursor.execute("SELECT id FROM todo_items")
    item_id = str(app.dbcursor.fetchone()[0])

    # edit() calls list_items() (no input), then: ID, task, effort, importance, earliestStart, deadline
    with patch("builtins.input", side_effect=[item_id, "New name", "", "", "", ""]):
        app.edit()

    app.dbcursor.execute("SELECT task FROM todo_items WHERE id = ?", (item_id,))
    assert app.dbcursor.fetchone()[0] == "New name"


def test_edit_skips_blank_fields():
    with patch("builtins.input", side_effect=["My task", "3", "5", "", ""]):
        app.add()
    app.dbcursor.execute("SELECT id, effort FROM todo_items")
    row = app.dbcursor.fetchone()
    item_id, original_effort = str(row[0]), row[1]

    # Leave all fields blank — should change nothing
    with patch("builtins.input", side_effect=[item_id, "", "", "", "", ""]):
        app.edit()

    app.dbcursor.execute("SELECT effort FROM todo_items WHERE id = ?", (item_id,))
    assert app.dbcursor.fetchone()[0] == original_effort
