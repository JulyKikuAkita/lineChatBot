import os
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
import pytest

import bot.wishes as birthday_module

# Patch BIRTHDAY_FILE before importing
TEMP_DIR = tempfile.mkdtemp()
TEST_BIRTHDAY_FILE = Path(TEMP_DIR) / "birthdays.json"

# Patch the module's BIRTHDAY_FILE to point to test file
birthday_module.BIRTHDAY_FILE = TEST_BIRTHDAY_FILE


@pytest.fixture(autouse=True)
def clean_birthdays_file():
    # Clean the file before each test
    if TEST_BIRTHDAY_FILE.exists():
        TEST_BIRTHDAY_FILE.unlink()
    yield
    if TEST_BIRTHDAY_FILE.exists():
        TEST_BIRTHDAY_FILE.unlink()


def test_handle_birthday_message_valid():
    msg = "記住 3月29日 是媽媽生日"
    result = birthday_module.handle_birthday_message(msg)
    assert "🐶 嗷嗚～我記住啦！媽媽 的生日是 3/29，到時我會送上狗狗的祝福喔！" in result

    data = birthday_module.load_birthdays()
    assert data["媽媽"] == "3/29"


def test_handle_birthday_message_invalid_format():
    msg = "生日是媽媽 3/29"
    result = birthday_module.handle_birthday_message(msg)
    assert "汪？我聽不懂這句話呢，可以問我記得誰的生日？" in result


def test_check_stored_birthday():
    birthday_module.save_birthdays({"爸爸": "04/01"})
    msg = "爸爸的生日是幾號？"
    result = birthday_module.handle_birthday_message(msg)
    assert "爸爸 的生日是 04/01" in result


def test_check_today_birthdays(monkeypatch):
    today = datetime.now().strftime("%m/%d")
    birthday_module.save_birthdays({"哥哥": today})
    result = birthday_module.check_today_birthdays()
    assert any("哥哥" in msg for msg in result)


def teardown_module(module):
    shutil.rmtree(TEMP_DIR)
