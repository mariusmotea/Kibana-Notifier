#!/usr/bin/python3
import docker
import json
import smtplib


smtp_server = "smtp.test.org"
recipients = ["marius.motea@test.org"]
subject = "Alert from Kibana"
sender_address = "elastic@test.org"

def sendMail(TEXT):
    """this is some test documentation in the function"""
    message = """\
From: %s
To: %s
Subject: %s

%s
""" % (sender_address, ", ".join(recipients), subject, TEXT)
    # Send the mail
    server = smtplib.SMTP(smtp_server)
    server.sendmail(sender_address, recipients, message)
    server.quit()


client = docker.from_env()
container = client.containers.get('kib01')

for line in container.logs(stream=True, tail=10):
    record = json.loads(line)
    if record["type"] == "log" and "error" in record["tags"]:
        sendMail(record["message"])
