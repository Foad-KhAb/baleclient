<p align="center">
  <img src="https://i.postimg.cc/Ssg1Tfhr/banner.png" alt="Aiobale Banner">
</p>

<h1 align="center">Aiobale</h1>
<h3 align="center">Async Python Client for Bale Messenger — Simplified, Modern, Pythonic</h3>

<p align="center">
  <strong>Aiobale</strong> is an asynchronous Python library that unlocks Bale Messenger's internal API, making it effortless to build bots, automation, and tools without diving into gRPC or Protobuf complexity.
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/aiobale?color=brightgreen&logo=pypi" alt="PyPI version">
  <img src="https://pepy.tech/badge/aiobale" alt="Downloads">
  <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-brightgreen?logo=python">
  <img src="https://img.shields.io/badge/License-MIT-blue?logo=open-source-initiative" alt="License">
</p>

---

## 🚀 Why Aiobale?

Bale Messenger's API can be a maze of encrypted gRPC calls. **Aiobale** cuts through the noise:

- Async-first, fully non-blocking, built on `aiohttp`.
- Type-safe Python classes for messages, users, groups, and more.
- Event-driven Dispatcher for clean, modular bot code.
- Handles connections, reconnections, and multi-client setups effortlessly.
- Reverse-engineered, continuously updated, zero reliance on `.proto` files.

**In short:** Build bots, automation, or monitoring tools **without wrestling with low-level network details**.

---

## ✨ Features

- **Async & High Performance:** Responsive bots and automation.
- **Complete API Coverage:** Messaging, files, presence, bots, groups, channels.
- **Pythonic Interface:** Type hints, dataclasses, clean methods.
- **Smart Dispatcher:** Decorator-based event routing, multiple clients support.
- **Robust Connections:** Auto-reconnects, handles disconnects gracefully.
- **Extensible & Modular:** Easy to adapt and extend for custom workflows.

---

## ⚠️ Important Notes

- Bale’s API is sensitive to excessive POST gRPC calls, especially outside authentication. Overuse may trigger **rate limits** or temporary account bans.
- Use Aiobale responsibly — **no spamming, scraping, or TOS violations**.
- Aiobale is **unofficial** and provided **as-is** for educational and ethical purposes.

---

## 📦 Installation

```bash
# Stable release
pip install aiobale

# Latest development version
pip install git+https://github.com/Enalite/aiobale.git
````

---

## 💡 Quick Start — Echo Bot

```python
from aiobale import Client, Dispatcher
from aiobale.types import Message

dp = Dispatcher()
client = Client(dp)

@dp.message()
async def echo(msg: Message):
    if content := msg.document:
        await msg.answer_document(content, use_own_content=True)
    elif text := msg.text:
        await msg.answer(text)
    else:
        await msg.answer("Nothing to echo!")

client.run()
```

---

## 🧑‍💻 Contributing

We welcome contributions of all kinds:

* ⭐ Star the repo
* 🐞 Report bugs or request features
* 🧩 Submit pull requests (code, docs, tests)
* ✍️ Help document unknown methods or structures

> Every contribution counts — even small fixes make a difference.

---

## 📄 License

Aiobale is released under the [MIT License](https://github.com/Enalite/aiobale/blob/main/LICENSE). Use freely and responsibly.

---

## 🔗 Links

* **PyPI:** [pypi.org/project/aiobale](https://pypi.org/project/aiobale)
* **GitHub:** [github.com/Enalite/aiobale](https://github.com/Enalite/aiobale)
* **Bale Channel:** [ble.ir/aiobale](https://ble.ir/aiobale)
* **Telegram Mirror:** [t.me/aiobale](https://t.me/aiobale)
* **Docs:** [docs.aiobale.ir](https://docs.aiobale.ir)

---

## 💬 Final Thoughts

Aiobale isn’t just a library — it’s a gateway to Bale Messenger’s inner workings.
Build bots, explore features, and automate with **confidence and simplicity**.

Welcome to the unofficial Bale ecosystem. Let’s innovate together!
