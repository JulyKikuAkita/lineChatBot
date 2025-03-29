import tempfile
import shutil
import json
from pathlib import Path
import pytest
import bot.memo as memory_module

# Setup
TEMP_DIR = tempfile.mkdtemp()
TEST_MEMORY_FILE = Path(TEMP_DIR) / "memory.json"

# Patch memory module
memory_module.MEMORY_FILE = TEST_MEMORY_FILE


@pytest.fixture(autouse=True)
def clean_memory_file():
    if TEST_MEMORY_FILE.exists():
        TEST_MEMORY_FILE.unlink()
    yield
    if TEST_MEMORY_FILE.exists():
        TEST_MEMORY_FILE.unlink()


def write_memory(data):
    with open(TEST_MEMORY_FILE, "w") as f:
        json.dump(data, f)


def test_store_key_value():
    msg = "記住 wifi 是 12345678"
    reply = memory_module.handle_memory_message(msg)
    assert "我會記得 wifi 是 12345678" in reply
    memory = memory_module.load_memory()
    assert memory["wifi"] == "12345678"


def test_query_known_key():
    write_memory({"地址": "台北市文山區"})
    reply = memory_module.handle_memory_message("地址是什麼")
    assert "地址 是 台北市文山區" in reply


def test_query_unknown_key():
    reply = memory_module.handle_memory_message("電話是什麼")
    assert "我沒有記得 電話 是什麼" in reply


def test_invalid_format_handling():
    reply = memory_module.handle_memory_message("記住 是 ")
    assert "格式是『記住 xxx 是 yyy』" in reply


def teardown_module(module):
    shutil.rmtree(TEMP_DIR)
