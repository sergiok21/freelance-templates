# Web Automation Framework

## Introduction
A Python-based automation framework designed to interact with web browsers, handle captchas, and integrate with external APIs such as **Kopeechka** and **SMS-Activate**.  
It provides a structured approach for automating account creation, data input, and verification workflows using configurable scripts and proxy support.

## Features
- **Browser Automation** – Automates browser interactions through a configurable core module.
- **Captcha Handling** – Integrated captcha-solving logic for bypassing verification steps.
- **API Integrations**:
  - **Kopeechka API** – Temporary email services for account registration.
  - **SMS-Activate API** – Virtual phone numbers for SMS verification.
- **Proxy Support** – Load and manage proxy lists for safe, distributed requests.
- **Multi-threading** – Run multiple browser automation tasks in parallel.
- **Configurable Workflows** – Adjustable parameters and behavior via configuration files.

## Project Structure
```
web-automation/
├── core/                # Core browser automation and captcha handling
│   ├── web.py
│   ├── dolphin.py
│   ├── captcha.py
│   └── base.py
├── services/            # External service integrations
│   ├── kopeechka.py
│   └── sms_activate.py
├── utils/               # Helper functions and system utilities
│   ├── files.py
│   ├── system.py
│   └── data.py
├── config.py            # Configuration file
├── main.py              # Entry point of the application
└── README.md
```

## Use Cases
- Automating account registration across multiple platforms.
- Handling email/SMS verification during sign-up processes.
- Captcha bypassing for automated workflows.
- Web testing scenarios that require repeated input/verification.

## Summary
This framework provides a solid base for building custom web automation scripts with integrated captcha-solving, proxy rotation, and API-based verification. It’s suitable for developers looking to streamline repetitive browser tasks or simulate user interactions on the web.
