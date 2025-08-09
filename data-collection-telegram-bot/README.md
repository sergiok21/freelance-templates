# Telegram Data Processing Bot

## Introduction
A Python-based Telegram bot built with **Aiogram** to automate the collection, searching, and management of user-submitted data (e.g., browser Cookies).  
It supports separate workflows for administrators and regular users, enabling efficient data handling for large user groups.

## Features
- **User Data Upload** – Users can send data (Cookies) individually or in bulk.  
- **Data Editing** – Users can download, modify, and re-upload their data.  
- **Admin Data Collection** – Administrators can compile all submitted data into archives.  
- **Search Functionality** – Search for a specific user by data signature (e.g., Cookie file name).  
- **Mass Messaging** – Send broadcast messages to all bot users who haven’t blocked the bot.  
- **Statistics** – View who has uploaded data and the number of accounts per user.

## Functionality
The bot has two primary modes:

1. **User Mode**  
   - Upload data files.  
   - Edit and re-upload updated files.  
   - Access usage instructions via `/help`.

2. **Admin Mode**  
   - Aggregate all user data into `results.zip` and `for_search.zip`.  
   - Perform keyword-based searches in uploaded data.  
   - View upload statistics.  
   - Send mass notifications.

**Core modules:**
- `admin.py` – Admin command handlers and logic.  
- `main.py` – User interactions and bot entry point.  
- `utils.py` – Helper functions for file processing and searches.  
- `config.py` – Bot initialization and settings.

## Usage
- Run the bot and interact via `/start` or `/help`.  
- Users upload and edit data via the provided keyboard options.  
- Admins use special menu commands for search, statistics, and broadcasts.

## Output
- **results.zip** – Compiled dataset from all users.  
- **for_search.zip** – Dataset prepared for search operations.

## Dependencies
- Python 3.8+
- [Aiogram](https://docs.aiogram.dev/)
- Standard library modules: `os`, `shutil`, `re`

## Use Cases
- Centralized collection of data from multiple remote users.  
- Quick identification of users by stored data signatures.  
- Coordinated communication with all participants in a network.

## Summary
This bot simplifies large-scale data collection, search, and management in a secure, automated manner, making it ideal for distributed teams or projects requiring user-contributed datasets.
