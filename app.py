import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template
from abuseipdb import check_ip
from emailer import send_alert

app = Flask(__name__)

# --- Logging Setup with Rotation ---
handler = RotatingFileHandler(
    "alerts.log", maxBytes=1_000_000, backupCount=5
)  # 1 MB per file, keep 5 backups
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    alert_message = None
    if request.method == "POST":
        ip = request.form.get("ip")
        if not ip:
            alert_message = "No IP address provided."
            logger.warning("Empty IP submitted.")
        else:
            result = check_ip(ip)

            if "error" in result:
                alert_message = f"Error: {result['error']}"
                logger.error(f"IP check failed for {ip}: {result['error']}")
            else:
                score = result.get("abuseConfidenceScore", 0)
                reports = result.get("totalReports", 0)

                if score > 50:
                    success = send_alert(ip, score, reports)
                    if success:
                        alert_message = f"Alert sent for {ip} (Score: {score})"
                        logger.info(f"Alert sent for {ip} | Score: {score} | Reports: {reports}")
                    else:
                        alert_message = f"Failed to send email alert for {ip}"
                        logger.error(f"Email send failed for {ip} | Score: {score} | Reports: {reports}")
                else:
                    alert_message = f"{ip} looks safe (Score: {score})"
                    logger.info(f"IP {ip} checked safe | Score: {score} | Reports: {reports}")

    # --- Read last 10 log entries ---
    try:
        with open("alerts.log", "r") as f:
            log_lines = f.readlines()
        recent_logs = log_lines[-10:]  # last 10 entries
    except FileNotFoundError:
        recent_logs = []

    return render_template("dashboard.html", alert_message=alert_message, recent_logs=recent_logs)

# --- Full Logs Route ---
@app.route("/logs")
def view_logs():
    try:
        with open("alerts.log", "r") as f:
            log_lines = f.readlines()
    except FileNotFoundError:
        log_lines = ["No logs yet."]
    return render_template("logs.html", logs=log_lines)

if __name__ == "__main__":
    app.run(debug=False)  # disable debugger PIN in production

