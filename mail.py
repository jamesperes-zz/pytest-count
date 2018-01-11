import smtplib

your_email = "EMAIL"
send_email = "EMAIL"

server = smtplib.SMTP('SMTP', 587)
server.starttls()
server.login(your_email, "PASSWORD")


def notification(number):
    server.connect()
    msg = "the number of errors in your code has increased to" + str(number)
    server.sendmail(your_email, send_email, msg)
    server.close()
    server.quit()
