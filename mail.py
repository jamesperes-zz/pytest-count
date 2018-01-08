import smtplib

your_email = ""
send_email = ""

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(your_email, "YOUR PASSWORD")


def notification(number):

    msg = "the number of errors in your code has increased to" + str(number)
    server.sendmail(your_email, send_email, msg)
    server.quit()
