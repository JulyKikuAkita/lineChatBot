import tempfile
import shutil
import json
from pathlib import Path
import pytest
import bot.notes as notes_module

# Setup
TEMP_DIR = tempfile.mkdtemp()
TEST_NOTES_FILE = Path(TEMP_DIR) / "notes.json"

# Patch note module
notes_module.NOTES_FILE = TEST_NOTES_FILE


@pytest.fixture(autouse=True)
def clean_notes_file():
    if TEST_NOTES_FILE.exists():
        TEST_NOTES_FILE.unlink()
    yield
    if TEST_NOTES_FILE.exists():
        TEST_NOTES_FILE.unlink()


def write_notes(data):
    with open(TEST_NOTES_FILE, "w") as f:
        json.dump(data, f)


def test_add_and_group_notes():
    # Add two notes from two users
    notes_module.handle_note_message("記住筆記：開會時間是週三 10:00", user_id="Alice")
    notes_module.handle_note_message("記住筆記：問房東租金", user_id="Bob")

    reply = notes_module.handle_note_message("/筆記清單", user_id="Alice")
    if reply is None:
        pytest.fail()
    assert "Alice" in reply
    assert "Bob" in reply
    assert "開會時間是週三" in reply
    assert "問房東租金" in reply


def test_delete_note_by_index():
    notes_module.handle_note_message("記住筆記：第一則", user_id="A")
    notes_module.handle_note_message("記住筆記：第二則", user_id="A")
    reply = notes_module.handle_note_message("刪除筆記 1", user_id="A")

    if reply is None:
        pytest.fail()
    assert "刪除了這則筆記" in reply
    remaining = notes_module.handle_note_message("/筆記清單")
    if remaining is None:
        pytest.fail()
    assert "第一則" not in remaining
    assert "第二則" in remaining


def test_empty_list_message():
    reply = notes_module.handle_note_message("/筆記清單")
    if reply is None:
        pytest.fail()
    assert "腦袋空空" in reply


def teardown_module(module):
    shutil.rmtree(TEMP_DIR)
