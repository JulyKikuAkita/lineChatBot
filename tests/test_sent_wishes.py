import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import pytest
import bot.sent_wishes as watcher_module

# Setup test file path
TEMP_DIR = tempfile.mkdtemp()
TEST_STATUS_FILE = Path(TEMP_DIR) / "birthday_sent_today.txt"

# Patch module
watcher_module.STATUS_FILE = TEST_STATUS_FILE


@pytest.fixture(autouse=True)
def clean_status_file():
    if TEST_STATUS_FILE.exists():
        TEST_STATUS_FILE.unlink()
    yield
    if TEST_STATUS_FILE.exists():
        TEST_STATUS_FILE.unlink()
    shutil.rmtree(TEMP_DIR)


def test_initial_state_should_be_false():
    assert watcher_module.has_already_sent_today() is False


def test_mark_and_check_same_day():
    watcher_module.mark_sent_today()
    assert watcher_module.has_already_sent_today() is True


def test_different_day_should_return_false(monkeypatch):
    yesterday = (datetime.now().replace(day=max(1, datetime.now().day - 1))).strftime("%Y-%m-%d")
    TEST_STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TEST_STATUS_FILE.write_text(yesterday)
    assert watcher_module.has_already_sent_today() is False
