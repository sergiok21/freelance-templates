## Встановлення

В проєкті застосовуються наступні інтеграції: Telegram, Google Cloud, Google Sheets, Clash of Clans API. Тому потрібно попередньо налаштувати усі сервіси.

### Google Cloud:

- Переходимо на сайт <b>[Google Cloud](https://console.cloud.google.com/)</b>.
- API & Services. 
- Створюємо проєкт (зліва зверху, біля Google Cloud). 
- Додаємо бібліотеки (Library): Google Sheets API, Google Drive API. 
- Повертаємось в API & Services, переходимо в Credentials і там: Create Credentials --> Service account --> Заповнюємо дані. 
- Переходимо у створений сервісний аккаунт (нижче у списку) --> Зберігаємо E-mail --> Keys -> Add key --> Create new key. Зберігаємо у JSON, в будь-яку папку (можна в папку проєкта). 
- Створюємо таблицю в Google Sheets --> Налаштування доступу --> Додаємо E-mail сервісного аккаунту.

### Clash of Clans API:

- Переходимо на сайт <b>[Clash of Clans for developers](https://developer.clashofclans.com/)</b>.
- Створюємо аккаунт на офіційному сайті.
- Переходимо в особистий аккаунт.
- Створюємо новий ключ із поточною публічною адресою.

### Налаштування проєкту:

- Завантажуємо проєкт:
```bash
git clone https://github.com/sergiok21/ternopil_telegram_bot.git
```
- Створюємо віртуальне середовище в папці з проєктом:
```bash
python -m venv venv
```
- Застосування у Windows:
```bash
./venv/Scripts/activate
```
для Unix-подібних:
```bash
source ./venv/bin/activate
```
- Завантажуємо залежності:
```bash
pip install -r requirements.txt
```
- <i>Додатково, якщо використовується PyCharm IDE: Налаштування --> Проєкт --> Python Interpreter --> Add Interpreter (local)...</i>
- Редагуємо `.env.example`-файл, та потім змінюємо назву на `.env`. Дані до заповнення:
```
BOT_TOKEN=...
CLASH_TOKEN=...
GROUP_ID=...
ADMINS=...
SHEET_CREDENTIALS=...
SHEET_URL=...
```
**Пояснення деяких полів `.env`:**\
`GROUP_ID` - можна отримати через бота.\
`ADMINS` - може записуватись через `123, 456`, цим самим адміністратором може бути не один користувач.\
`SHEET_CREDENTIALS` - повний шлях `.json`-файлу з Google Cloud.
`SHEET_URL` - посилання на таблицю (https://docs.google.com/spreadsheets/d/1ZX....23F/).

## Використання

Доступні наступні команди:

### 1. Для всіх учасників групи:
- `/add_account #TAG` — додавання акаунту в таблицю.

### 2. Для привілейованих учасників:
- `/create_poll` — створення опитування.
- `/empty_answers` — відображення користувачів, які не відповіли на опитування.
