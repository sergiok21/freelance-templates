# VMay Site — Photo Platform (Django + Clean Architecture)

## Introduction
**VMay Site** is a modular photography platform built with **Django** and organized using **Clean Architecture** principles.
The repository includes application code, infrastructure-as-code, and deployment tooling for a production-ready setup.

Core goals:
- Manage photo categories, content and public pages.
- Keep the backend testable and maintainable via clear layers (domain, use cases, adapters).
- Enable reproducible deployments with Docker, Ansible, and Terraform.
- Provide centralized logs/metrics via Promtail/Loki/Prometheus/Grafana.

## Features
- **Clean Architecture layout** (`pkg/` and `photo/` apps with adapters, frameworks, use cases).
- **Django web app** for photo content and categories.
- **Testing ready** (pytest structure under `photo/tests` and `pkg/tests`).
- **Containerized runtime** via `infrastructure/docker/docker-compose.yml`.
- **IaC & Automation**:
  - **Ansible** roles/playbooks for server provisioning and app rollout.
  - **Terraform** templates for cloud resources.
- **Observability**:
  - **Promtail** log shipping.
  - **Loki** log storage and query.
  - **Prometheus** metrics collection.
  - **Grafana** dashboards (configs under `infrastructure/monitoring`).

## Project Structure
```
vmay-site/
├── photo/                     # Django project & feature modules (Home, Portfolio, etc.)
│   ├── manage.py
│   ├── assets/                # Fixtures, media, static files
│   ├── photo/                 # Django project package (urls, settings wiring, etc.)
│   ├── category/              # Category module (Clean Architecture layers)
│   ├── extensions/            # Extensions for Django-apps (templates + templatetags, repositories, etc.)
│   ├── ...                    # Other Django-apps
│   └── tests/                 # Test suite
├── pkg/                       # Shared Clean Architecture scaffolding (app/use cases/adapters)
│   ├── application/
│   ├── interface_adapters/
│   ├── frameworks_drivers/
│   └── tests/
├── infrastructure/
│   ├── docker/                # docker-compose.yml and container configs
│   ├── ansible/               # Playbooks, roles, inventories
│   ├── terraform/             # .tf modules and envs
│   └── monitoring/            # loki / promtail / prometheus configs
└── README.md
```

## Deployment
- **Ansible**: run playbooks in `infrastructure/ansible` to provision servers, deploy containers, and sync configs.
- **Terraform**: provision cloud resources (networks, VMs, buckets) using modules in `infrastructure/terraform`.

## Monitoring & Logging
- **Promtail** collects logs from containers.
- **Loki** stores logs and provides querying.
- **Prometheus** scrapes metrics.
- **Grafana** dashboards can visualize both logs and metrics.

## Summary
This repository combines **Django + Clean Architecture** application code with a production-minded toolchain (Docker, Ansible, Terraform, and observability stack).  
It’s suitable as a foundation for a photo-driven site with clear separation of concerns, automated deployments, and centralized monitoring.
