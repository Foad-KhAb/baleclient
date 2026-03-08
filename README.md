# BaleClient

⚡ **BaleClient** is a maintained fork / rework of **Aiobale**, an asynchronous Python client for **Bale Messenger**.

The original library is great but contains several bugs and incomplete implementations.
This project fixes those issues and adds improvements for reliability, stability, and usability.

---

## Installation

Install from PyPI:

```bash
pip install baleclient
```

Upgrade to the latest version:

```bash
pip install -U baleclient
```

Install from source:

```bash
git clone https://github.com/Foad-KhAb/baleclient.git
cd baleclient
pip install -e .
```

---

## Requirements

* Python **3.11+**

---

## Quick Example

```python
from baleclient import Client

async def main():
    async with Client("session") as client:
        me = await client.get_me()
        print(me)
```

---

## Features

* Fully **asynchronous** API
* Lightweight and fast
* Improved parsing reliability
* Better error handling
* Maintained fork of Aiobale

---

## Based On

This project is based on:

**Aiobale**
https://github.com/Enalite/aiobale

Credit to the original author for the initial implementation.

---

## Why BaleClient?

While using Aiobale in real projects, I encountered several issues such as:

* parsing bugs
* inconsistent API responses
* missing validations
* edge cases not handled

**BaleClient** fixes these problems and introduces improvements to make the library more stable for production usage.

---

## Fixes

List of fixes applied to the original library:

* [x] Fix dialog response parsing
* [x] Fix message caption parsing
* [x] Fix incorrect type validations

*(this list will grow as more issues are discovered)*

---

## Added Improvements

Additional features and improvements:

* [x] Better error handling when reading corrupted or modified session files

---

## Changelog

### v0.1.0

* Initial release
* Fork of Aiobale with several fixes
* Improved session error handling

---

## Documentation

Documentation will be expanded in future releases.

For now, refer to:

* The source code
* Example usage in the repository

---

## Notes

* BaleClient is **not an official Bale API library**
* The Bale API is internal and may change without notice

---

## License

This project follows the same license as the original project unless otherwise specified.
