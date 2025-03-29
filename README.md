# 🐶 FamilyLineDogBot

A LINE chatbot with a loyal dog personality, built for family groups to:

- 🎂 Remember and celebrate birthdays
- 📆 Summarize weekly group activity
- 🐾 Respond in a cute dog voice

---

## 🚀 Features

- Keyword-based birthday memory (`記住 3月29日 是媽媽生日`)
- Friendly birthday lookup (`媽媽生日是幾號？`)
- Auto summary of weekly group messages
- Cute dog-style responses like `汪！我記住啦！`
- Testable, modular, GitHub-friendly

---

## 🛠 Setup

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

---

## 🧪 Run Tests

```bash
make test
```

---

## 🎨 Format & Lint

```bash
make format
make lint
```

---

## 📁 Project Structure

```
bot/
  birthday.py          # Birthday logic
  messageHistory.py    # Message logging and summary
  main.py              # Webhook handler (Flask)
  resources/
    birthdays.json     # Stored birthday data (gitignored)

tests/
  test_birthday.py     # Unit tests for birthday features
  test_logger.py       # Unit tests for message history

.github/workflows/
  python-tests.yml     # GitHub Actions CI

requirements.txt       # Project dependencies
pyproject.toml         # Formatter config
Makefile               # Dev tools shortcut
README.md              # You're reading it!
```

---

## 🐾 Personality

This bot speaks in a loyal, friendly dog tone — perfect for warm, fun family interactions.  
You can customize the voice/personality to match your family style.

---

## 🤖 Hosted on Replit, GitHub-friendly, CI-ready!

## Read more about line API
https://github.com/line/line-bot-sdk-python/blob/master/README.rst

# Deployed at
https://replit.com/@banananoonoodle/FamilyLineChatBot