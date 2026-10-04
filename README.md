
# Password Strength Analyzer & Security Suggestion Tool

A privacy-focused defensive cybersecurity application that analyzes password strength, detects predictable patterns, evaluates password policies, and provides actionable security recommendations.

**Developed by:** Ayush Kumar Dubey

---

## Overview

The Password Strength Analyzer & Security Suggestion Tool is an educational cybersecurity project designed to help users understand password weaknesses and improve their password security practices.

The application evaluates password length, character diversity, common-password usage, predictable sequences, repeated patterns, dictionary words, and other weaknesses.

It also provides a cryptographically secure password generator, an educational Argon2id hashing demonstration, and an optional privacy-conscious analysis history.

The analysis engine processes passwords locally through the Flask backend. Submitted passwords are not intentionally stored in the database or written to application logs.

> **Important:** Use synthetic or demonstration passwords while testing. Do not enter your actual personal, banking, email, or institutional passwords.

---

## Key Features

### Password Analysis
- Real-time password strength evaluation.
- Five strength classifications:
  - VERY WEAK
  - WEAK
  - MODERATE
  - STRONG
  - VERY STRONG
- Password length analysis.
- Lowercase, uppercase, digit, and symbol diversity analysis.
- Common password detection using a local dataset.
- Sequential character and keyboard-pattern detection.
- Repeated character and substring detection.
- Predictable prefix, suffix, year, and date detection.
- Local dictionary-word detection.
- Educational entropy estimation.
- Actionable security recommendations.

### Secure Password Generator
- Uses Python's `secrets` module.
- Configurable password length.
- Optional lowercase, uppercase, digit, and symbol categories.
- Ensures at least one character from every selected category.

### Password Policy Checker
- Evaluates passwords against the application's default password policy.
- Checks minimum length and character diversity.
- Identifies common and predictable password patterns.
- Returns compliance status and recommendations.

### Privacy-First Analysis History
- History is saved only after an explicit user action.
- Stores approved analysis metadata only.
- Supports viewing and clearing saved records.
- Does not intentionally store plaintext passwords or password hashes.

### Educational Argon2id Demonstration
- Demonstrates password hashing using Argon2id.
- Demonstrates password verification.
- Explains the difference between password analysis and password hashing.
- Hashes are returned for educational demonstration and are not persisted by these endpoints.

### Visual Dashboard
- Responsive HTML, CSS, and JavaScript interface.
- Score visualization using Chart.js.
- Analysis metrics and security suggestions.
- Show/hide password functionality.
- Password generator interface.
- Optional history dashboard.

### Security and Testing
- Flask API rate limiting.
- Security response headers.
- Production secret-key validation.
- Privacy regression tests.
- Dependency vulnerability auditing with pip-audit.
- Python security analysis with Bandit.
- Automated GitHub Actions workflow.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML5, CSS3, JavaScript |
| Database | SQLite |
| Visualization | Chart.js |
| Password generation | Python `secrets` |
| Password hashing demonstration | Argon2id |
| API documentation | OpenAPI, Swagger UI |
| Testing | Pytest |
| Security auditing | Bandit, pip-audit |
| Version control | Git, GitHub |
| CI/CD | GitHub Actions |

---

## Project Architecture

```text
Password-Strength-Analyzer/
│
├── .github/
│   └── workflows/
│       └── security-ci.yml
│
├── backend/
│   ├── routes/
│   │   ├── analyzer.py
│   │   ├── generator.py
│   │   ├── policy.py
│   │   ├── history.py
│   │   ├── hash_demo.py
│   │   ├── docs.py
│   │   ├── frontend.py
│   │   └── health.py
│   │
│   ├── services/
│   │   ├── password_analyzer.py
│   │   ├── password_generator.py
│   │   ├── password_policy_checker.py
│   │   ├── entropy_estimator.py
│   │   ├── common_password_checker.py
│   │   ├── dictionary_word_detector.py
│   │   ├── pattern_detector.py
│   │   ├── repetition_analyzer.py
│   │   ├── predictable_pattern_analyzer.py
│   │   ├── history_service.py
│   │   └── argon2_demo.py
│   │
│   ├── config.py
│   ├── extensions.py
│   ├── app.py
│   └── __init__.py
│
├── data/
│   ├── common_passwords.txt
│   └── common_words.txt
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── index.html
│
├── tests/
│
├── docs/
│   ├── API_REFERENCE.md
│   └── SECURITY_AND_PRIVACY.md
│
├── reports/
├── screenshots/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

---

## Installation and Setup

### Prerequisites

- Python 3.11 or later.
- Git.
- Visual Studio Code (recommended).
- A modern web browser.

### 1. Clone the repository

```bash
git clone https://github.com/ayushkrdubey-23/Password-Strength-Analyzer.git
cd Password-Strength-Analyzer
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### 4. Configure environment variables

```powershell
Copy-Item .env.example .env
```

For local development, review the `.env` configuration and keep:

```env
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=5000
DATABASE_PATH=instance/analytics.db
```

For production, configure a unique, securely generated `APP_SECRET_KEY` and set `APP_ENV=production`.

### 5. Start the application

```bash
python -m backend.app
```

Open the application:

```text
http://127.0.0.1:5000/
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:5000/apidocs
```

OpenAPI specification:

```text
http://127.0.0.1:5000/openapi.json
```

Detailed endpoint documentation and request examples are available in:

[`docs/API_REFERENCE.md`](docs/API_REFERENCE.md)

---

## Running Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

Compile backend and test files:

```bash
python -m compileall backend tests
```

Run Bandit:

```bash
bandit -r backend -ll
```

Audit dependencies:

```bash
pip-audit
```

Check frontend JavaScript syntax:

```bash
node --check frontend/js/app.js
```

---

## GitHub Actions

The repository includes a GitHub Actions workflow that runs on pushes and pull requests targeting `main`.

The workflow performs:

- Python environment setup.
- Dependency installation.
- Python compilation.
- Automated tests.
- Bandit security analysis.
- pip-audit dependency checks.
- Frontend JavaScript syntax validation.

Check the **Actions** tab in the GitHub repository for workflow execution results.

---

## Privacy and Security

This project follows a privacy-conscious educational design:

- Submitted passwords are processed transiently.
- The analysis API does not intentionally return submitted passwords.
- Passwords are not intentionally stored in SQLite.
- Analysis history accepts only approved metadata fields.
- Password generation uses Python's cryptographically secure `secrets` module.
- The Argon2id demonstration does not persist passwords or generated hashes.
- Local datasets are used for common-password and dictionary checks.

Read [`docs/SECURITY_AND_PRIVACY.md`](docs/SECURITY_AND_PRIVACY.md) for the detailed design and limitations.

---

## Project Limitations

This is an educational, single-user project and is not a production authentication platform.

- It does not authenticate users or isolate history between multiple users.
- The current rate limiter uses in-memory storage.
- Entropy estimates are theoretical approximations and do not guarantee resistance to attacks.
- Local wordlists are limited and cannot identify every weak password.
- Frontend visualizations and Swagger UI use external CDNs.
- The application does not replace a professional password manager or a properly implemented authentication system.

---

## Screenshots

Application screenshots will be maintained in the `screenshots/` directory.

Suggested screenshots:

- `01-home-dashboard.png`
- `02-password-analysis.png`
- `04-security-suggestions.png`
- `05-password-generator.png`
- `07-analysis-history.png`
- `08-swagger-api-docs.png`

---

## Learning Outcomes

Through this project, the following concepts are explored:

- Defensive cybersecurity and password security.
- Password-strength heuristics and pattern detection.
- Password entropy estimation.
- Cryptographically secure random generation.
- Password hashing with Argon2id.
- REST API development using Flask.
- SQLite database integration.
- Secure handling of sensitive inputs.
- Automated testing and privacy regression testing.
- Dependency auditing and static security analysis.
- GitHub Actions CI automation.

---

## Author

**Ayush Kumar Dubey**

GitHub: [@ayushkrdubey-23](https://github.com/ayushkrdubey-23)

Project Repository: [Password Strength Analyzer & Security Suggestion Tool](https://github.com/ayushkrdubey-23/Password-Strength-Analyzer-Security-Tool)

---

## Disclaimer

This application is developed for educational and defensive cybersecurity purposes. It is not intended to collect, store, expose, or misuse real user passwords.
