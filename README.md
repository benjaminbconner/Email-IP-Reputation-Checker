# Email-IP-Reputation-Checker
A Flask web app that checks email server IPs against AbuseIPDB, sends Outlook alerts, and logs results.

## Features
- Check IP reputation via AbuseIPDB API
- Email alerts sent through Outlook.com SMTP
- Logs stored in `alerts.log`
- Web dashboard with recent checks

Repo Structure

email_alert_app/
├── app.py
├── abuseipdb.py
├── emailer.py
├── templates/
│   └── dashboard.html
├── requirements.txt
├── README.md
├── .gitignore
└── .env.example   ← safe to share
