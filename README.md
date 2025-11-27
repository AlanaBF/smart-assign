# Flowcase ETL & Smart-Assign

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Tech stack

Backend: Python 3.10+, FastAPI, SQLAlchemy, Uvicorn

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![FastAPI](https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

Frontend: Angular (latest v20+), TypeScript, Tailwind

[![Angular](https://img.shields.io/badge/Angular-%23DD0031.svg?logo=angular&logoColor=white)](https://angular.io/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=fff)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-%2338B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

Database: PostgreSQL (12+)

[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)

Dev tooling: npm, node 18+, pip, virtualenv/venv

[![npm](https://img.shields.io/badge/npm-CB3837?logo=npm&logoColor=fff)](https://www.npmjs.com/)

## About

This repository contains three components used together:

- `flowcase_etl/` — an external repo - ETL pipeline that produces the Postgres data model.
- `backend/` — FastAPI service that reads the ETL database.
- `frontend/smart-assign/` — Angular UI that calls the backend API.

For setup and development, use the per-project README files:

- Backend: `backend/README.md`
- Frontend: `frontend/smart-assign/README.md`
- ETL pipeline: [`flowcase_etl/README.md`](https://github.com/AlanaBF/etl_pipeline)

## Repository layout

```text
./
├─ flowcase_etl/        # (external repo) ETL pipeline producing DB schema/data
├─ backend/             # FastAPI service, `backend/README.md` for details
└─ frontend/smart-assign/ # Angular app, `frontend/smart-assign/README.md` for details
```

## Get the code

### Clone the Smart-Assign repository

```bash
git clone https://github.com/AlanaBF/smart-assign.git
cd smart-assign
```

This overview only shows how to fetch the source. See each project's README for setup and run instructions.

Note: do not commit `backend/.env` or other secret files. Copy `backend/.env.example` and fill in your credentials locally.

### Clone the ETL repository (PostgreSQL data model)

```bash
git clone https://github.com/AlanaBF/etl_pipeline.git
```

See the ETL repo README for details on preparing the Postgres database and running the pipeline.

## Secrets & security

- Keep `.env` and other secret files out of source control. Use `.gitignore` to prevent accidental commits.
- Rotate database credentials if any secret leaks are suspected.

## Screenshots

COMING SOON

## License & contact

- This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
- Questions or access issues: contact the repository owner.

## Questions

Have questions? Get in touch:

- [![Email](https://img.shields.io/badge/Email-alanabarrett--frew%40hotmail.com-0052CC?style=flat&logo=gmail&logoColor=white)](mailto:alanabarrett-frew@hotmail.com)

- [![GitHub](https://img.shields.io/badge/GitHub-@AlanaBF-181717?style=flat&logo=github&logoColor=white)](https://github.com/AlanaBF)

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Alana%20Barrett%20Frew-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alanabarrettfrew/)
