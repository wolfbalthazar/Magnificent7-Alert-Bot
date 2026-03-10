import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Betöltjük az .env fájl tartalmát
load_dotenv()

# --- BEÁLLÍTÁSOK ---
# Ezek az értékek most már az .env fájlból jönnek
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
# --------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465 # SSL port

def send_email(subject: str, html_body: str):
    """
    Sends an email using the provided SMTP credentials.
    """
    if SENDER_EMAIL == "test_sender@example.com":
         print(f"--- MOCK EMAIL SENDER ---")
         print(f"To: {RECEIVER_EMAIL}")
         print(f"Subject: {subject}")
         print(f"Body: \n{html_body}")
         print(f"-------------------------")
         return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
        # Use SMTP_SSL for port 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print(f"Email successfully sent to {RECEIVER_EMAIL}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def format_rsi_alert(ticker: str, current_price: float, rsi_value: float) -> tuple[str, str]:
    """
    Formats the subject and HTML body for an RSI indicator alert.
    """
    subject = f"🚨 Tőzsdei Riasztás: {ticker} RSI Túladott (<30)"
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #d13a3a;">RSI Túladottság Jelzés!</h2>
        <p>A(z) <strong>{ticker}</strong> részvény 30 perces grafikonján az RSI 30 alá esett.</p>
        <table style="border-collapse: collapse; width: 100%; max-width: 400px; margin-top: 20px;">
          <tr style="background-color: #f2f2f2;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Adat</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Érték</th>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Jelenlegi Ár</td>
            <td style="padding: 10px; border: 1px solid #ddd;"><b>${current_price:.2f}</b></td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Jelenlegi RSI</td>
            <td style="padding: 10px; border: 1px solid #ddd;"><b style="color: #d13a3a;">{rsi_value:.2f}</b></td>
          </tr>
        </table>
        <p style="margin-top: 20px;"><i>Ez egy automatikus üzenet a Python Tőzsdefigyelő programodból.</i></p>
      </body>
    </html>
    """
    return subject, body

def format_ma_alert(ticker: str, current_price: float, fast_ma: float, slow_ma: float) -> tuple[str, str]:
    """
    Formats the subject and HTML body for a Moving Average crossover alert.
    """
    subject = f"📈 Tőzsdei Riasztás: {ticker} MA Kereszteződés (Golden Cross)"
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color: #2e8b57;">Mozgóátlag Kereszteződés!</h2>
        <p>A(z) <strong>{ticker}</strong> részvény 30 perces grafikonján a gyors mozgóátlag (MA 20) alulról felfelé metszette a lassút (MA 50).</p>
        <table style="border-collapse: collapse; width: 100%; max-width: 400px; margin-top: 20px;">
          <tr style="background-color: #f2f2f2;">
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Adat</th>
            <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Érték</th>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Jelenlegi Ár</td>
            <td style="padding: 10px; border: 1px solid #ddd;"><b>${current_price:.2f}</b></td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Gyors MA (20)</td>
            <td style="padding: 10px; border: 1px solid #ddd;">${fast_ma:.2f}</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Lassú MA (50)</td>
            <td style="padding: 10px; border: 1px solid #ddd;">${slow_ma:.2f}</td>
          </tr>
        </table>
        <p style="margin-top: 20px;"><i>Ez egy automatikus üzenet a Python Tőzsdefigyelő programodból.</i></p>
      </body>
    </html>
    """
    return subject, body

if __name__ == "__main__":
    # Test formatting and mockup sender
    subj_rsi, body_rsi = format_rsi_alert("AAPL", 150.25, 28.5)
    send_email(subj_rsi, body_rsi)
    
    subj_ma, body_ma = format_ma_alert("MSFT", 320.10, 315.5, 314.2)
    send_email(subj_ma, body_ma)
