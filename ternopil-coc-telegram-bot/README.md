# Clash of Clans Telegram Bot

## Installation

This project integrates with the following services: Telegram, Google Cloud, Google Sheets, and Clash of Clans API.  
You need to configure all these services beforehand.

### Google Cloud:

- Go to <b>[Google Cloud](https://console.cloud.google.com/)</b>.
- Navigate to **API & Services**.
- Create a project (top left, next to the Google Cloud logo).
- Add libraries (Library): **Google Sheets API**, **Google Drive API**.
- Go back to **API & Services**, go to **Credentials** and: Create Credentials → Service account → Fill in the details.
- Open the created service account (listed below) → Save the **E-mail** → **Keys** → **Add key** → **Create new key**.  
  Save it as JSON in any folder (you can place it in the project folder).
- Create a spreadsheet in Google Sheets → **Share settings** → Add the service account email.

### Clash of Clans API:

- Go to <b>[Clash of Clans for developers](https://developer.clashofclans.com/)</b>.
- Create an account on the official site.
- Go to your personal account.
- Create a new key with your current public IP address.

### Project Setup:

- Download the project:
```bash
git clone https://github.com/sergiok21/ternopil_telegram_bot.git
```
- Create a virtual environment in the project folder:
```bash
python -m venv venv
```
- For Windows:
```bash
./venv/Scripts/activate
```
- For Unix-like systems:
```bash
source ./venv/bin/activate
```
- Install dependencies:
```bash
pip install -r requirements.txt
```
- *Optional, if using PyCharm IDE*: Settings → Project → Python Interpreter → Add Interpreter (local)...
- Edit the `.env.example` file and rename it to `.env`. Fill in the following fields:
```
BOT_TOKEN=...
CLASH_TOKEN=...
GROUP_ID=...
ADMINS=...
SHEET_CREDENTIALS=...
SHEET_URL=...
```
**Explanation of some `.env` fields:**  
`GROUP_ID` – can be obtained via the bot.  
`ADMINS` – can be written as `123,456`, allowing multiple admins.  
`SHEET_CREDENTIALS` – full path to the `.json` file from Google Cloud.  
`SHEET_URL` – spreadsheet link (https://docs.google.com/spreadsheets/d/1ZX....23F/).

## Usage

Available commands:

### 1. For all group members:
- `/add_account #TAG` — add an account to the table.

### 2. For privileged members:
- `/create_poll` — create a poll.
- `/empty_answers` — display users who have not responded to the poll.
