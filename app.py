import logging
from flask import Flask, request, render_template
from abuseipdb import check_ip
from emailer import send_alert

app = Flask(__name__)

# --- Logging Setup ---
logging.basicConfig(
    filename="alerts.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    alert_message = None
    if request.method == "POST":
        ip = request.form.get("ip")
        result = check_ip(ip)

        if "error" in result:
            alert_message = f"Error: {result['error']}"
            logging.error(f"IP check failed for {ip}: {result['error']}")
        else:
            score = result.get("abuseConfidenceScore", 0)
            reports = result.get("totalReports", 0)

            if score > 50:
                success = send_alert(ip, score, reports)
                if success:
                    alert_message = f"Alert sent for {ip} (Score: {score})"
                    logging.info(f"Alert sent for {ip} | Score: {score} | Reports: {reports}")
                else:
                    alert_message = f"Failed to send email alert for {ip}"
                    logging.error(f"Email send failed for {ip} | Score: {score} | Reports: {reports}")
            else:
                alert_message = f"{ip} looks safe (Score: {score})"
                logging.info(f"IP {ip} checked safe | Score: {score} | Reports: {reports}")

    # --- Read last 10 log entries ---
    try:
        with open("alerts.log", "r") as f:
            log_lines = f.readlines()
        recent_logs = log_lines[-10:]  # last 10 entries
    except FileNotFoundError:
        recent_logs = []

    return render_template("dashboard.html", alert_message=alert_message, recent_logs=recent_logs)

if __name__ == "__main__":
    app.run(debug=True)
