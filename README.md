# Balethon

Balethon is a maintained fork / rework of **Aiobale**, an asynchronous Python client for Bale Messenger.

The original library is great but contains several bugs and incomplete implementations.
This project fixes those issues and adds additional improvements for reliability and usability.

Balethon is used internally in Chavosh projects and will continue to receive fixes and improvements.

---

## Based On

This project is based on:

**Aiobale**
https://github.com/Enalite/aiobale

Credit to the original author for the initial implementation.

---

## Why Balethon?

While using Aiobale in real projects, I encountered several issues such as:

- parsing bugs
- inconsistent API responses
- missing validations
- edge cases not handled

Balethon fixes these problems and adds additional improvements.

---

## Fixes

List of fixes applied to the original library:

- [X] Fix dialog response parsing
- [X] Fix message caption parsing
- [X] Fix incorrect type validations

*(this list will grow as more issues are discovered)*

---

## Added Improvements

Additional features and improvements:

- [X] Better error handling in reading corrupted or changed session files


---

## Notes

* Balethon is **not an official Bale API library**.
* The Bale API is internal and may change without notice.

---
