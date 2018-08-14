def emailhelp():
    print ("Functions:")
    print()
    print ("outlooksimple(ffrom, tto(list of emails), login, password, subject,")
    print ("     file(True/False for if a file is to be read for body of mail),")
    print("     message(either a .txt file in string form or a string for the ")
    print("     body of mail)")
    print()
    print ("emailhelp()")
    print()
def outlooksimple(ffrom, tto, login, password, subject, file, message):
                
    import smtplib as smtp
    from email.mime.text import MIMEText

    
    if file==True:
        with open(message, 'r') as fp:
            text=fp.read()
    else:
        text = message
    msg = MIMEText(text)

    msg['Subject'] = subject
    msg['From'] = ffrom
    msg['To'] = ",".join(tto)


    s = smtp.SMTP("smtp-mail.outlook.com")
    s.starttls()
    s.login(login, password)
    s.sendmail(ffrom, tto, msg.as_string())
