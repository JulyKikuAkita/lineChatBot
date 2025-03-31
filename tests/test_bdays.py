import shutil
import tempfile
import json
from pytz import timezone
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
    assert result is None


def test_check_stored_birthday():
    birthday_module.save_birthdays({"爸爸": "04/01"})
    msg = "爸爸的生日是幾號？"
    result = birthday_module.handle_birthday_message(msg)
    assert "爸爸 的生日是 04/01" in result


def test_check_today_birthdays(monkeypatch):
    today = datetime.now(timezone("Asia/Taipei")).strftime("%m/%d")
    birthday_module.save_birthdays({"哥哥": today})
    result = birthday_module.check_today_birthdays_custom()
    assert any("哥哥" in msg for msg in result)


def test_birthday_match_today(monkeypatch):
    today = datetime.now(timezone("Asia/Taipei")).strftime("%m/%d")
    emojis = "🎉🐾🎂🎁💖🍰🧁🎊🌟✨🎈🐶🐹🐰🐻🪅🎇🎆"
    with open(TEST_BIRTHDAY_FILE, "w") as f:
        json.dump({"媽媽": today}, f)

    messages = birthday_module.check_today_birthdays_custom()
    assert len(messages) >= 1
    for msg in messages:
        lines = msg.splitlines()
        if len(lines) > 1:
            assert len(lines) == 3, "訊息應包含上框、中間、下框三行"
            assert "媽媽" in lines[1], "中間行應包含壽星名字"
            assert all(c in emojis for c in lines[0]), "上框包含應有 emoji"
            assert all(c in emojis for c in lines[2]), "下框包含應有 emoji"
            assert len(lines[0]) == len(lines[2]), "上框寬度應與下框寬度一致"


def test_birthday_no_match():
    with open(TEST_BIRTHDAY_FILE, "w") as f:
        json.dump({"爸爸": "01/01"}, f)

    messages = birthday_module.check_today_birthdays_custom()
    assert messages == []


def teardown_module(module):
    shutil.rmtree(TEMP_DIR)
