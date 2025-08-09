# Web Car Parser Platform

## Introduction
**Web Car Parser** is a modular, Docker-based platform for collecting, processing, and managing car-related data from various web sources.  
It integrates a **Django-powered backend**, a **Telegram bot** for user and admin interactions, and a **parser service** to automate data extraction.  
The system includes built-in monitoring with **Prometheus**, **Loki**, and **Grafana**, as well as deployment automation via **Ansible**.

## Features
- **Automated Car Data Parsing** – Extract and process vehicle data from online sources.
- **Django Web Backend** – REST API and admin panel for managing parsed data.
- **Telegram Bot Integration** – Two-way communication with users and admins for control, updates, and notifications.
- **Task Scheduling** – Automated start/stop of parsing jobs.
- **Monitoring Stack** – Integrated **Loki**, **Promtail**, and **Prometheus** for system logs and metrics.
- **Deployment Automation** – Ansible playbooks for server provisioning and updates.
- **Docker Orchestration** – Each service is containerized for scalability and easy deployment.

## Project Structure
```
web-car-parser/
├── web/             # Django web application
├── parser/          # Parsing service (Django + scheduled jobs)
├── telegram/        # Telegram bot and related services
├── monitor/         # Monitoring stack configuration (Loki, Promtail, Prometheus)
├── ansible/         # Deployment automation playbooks and roles
├── docker-compose.yml
└── README.md
```

## Use Cases
- Aggregating and managing vehicle listings from multiple online marketplaces.
- Providing real-time updates to users via Telegram.
- Automating car market data analysis for dealerships or analysts.

## Summary
The Web Car Parser Platform offers an end-to-end solution for automated car data collection and management.  
Its modular design, monitoring capabilities, and deployment automation make it suitable for production environments where scalability and reliability are essential.
