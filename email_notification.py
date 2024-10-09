import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(receiver_email, job_details):
    sender_email = "your_email@gmail.com"
    password = "your_email_password"

    # Setting up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Job Application Notification"

    # Create the body of the message
    body = f"Hi there,\n\nYou have successfully applied to the following job(s):\n\n{job_details}\n\nBest of luck!\nCareer Accelerator Bot"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")