import tempfile
import shutil
from datetime import datetime
from pathlib import Path

import pytest
import bot.messageHistory as logger_module

# Setup temporary log file path
TEMP_DIR = tempfile.mkdtemp()
TEST_LOG_FILE = Path(TEMP_DIR) / "message_log.json"

# Patch logger module
logger_module.LOG_FILE = TEST_LOG_FILE


@pytest.fixture(autouse=True)
def clean_log_file():
    if TEST_LOG_FILE.exists():
        TEST_LOG_FILE.unlink()
    yield
    if TEST_LOG_FILE.exists():
        TEST_LOG_FILE.unlink()


def test_log_and_load_message():
    logger_module.log_message("user1", "Hello world!")
    log = logger_module.load_log()
    assert len(log) == 1
    assert log[0]["user"] == "user1"
    assert log[0]["text"] == "Hello world!"


def test_get_weekly_summary_with_data(monkeypatch):
    now = datetime.now().isoformat()
    messages = [
        {"user": "Alice", "text": "會議時間是週三", "timestamp": now},
        {"user": "Bob", "text": "房子看起來不錯", "timestamp": now},
    ]
    with open(TEST_LOG_FILE, "w") as f:
        import json

        json.dump(messages, f)

    summary = logger_module.get_weekly_summary()
    assert "最活躍的是：Alice" in summary
    assert "訊息統計：\n- 總共有 2 則訊息被記錄下來" in summary


def test_get_weekly_summary_empty():
    summary = logger_module.get_weekly_summary()
    assert "這週" in summary or "安靜" in summary


def teardown_module(module):
    shutil.rmtree(TEMP_DIR)
