from jira import JIRA
import csv
from datetime import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailException(Exception):
    def __init__(self, text):
        self.txt = text

def mail_send(issues, receiverMail,senderMail, password):
    html = f"""
        <html>
        <head></head>
        <body>
            <p>{issues}</p>
        </body>
        </html>
        """
    text = ""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Напоминание о задачах"
    msg['From'] = senderMail
    msg['To'] = receiverMail
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    mail = smtplib.SMTP('smtp.yandex.ru', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(senderMail, password)
    mail.sendmail(senderMail, receiverMail, msg.as_string())
    mail.quit()

data = open('data.txt','r+')

if data.readline() == '' :
    data.write(input('Введите почту, с которой будет производится отправка: ')+'\n')
    data.write(input('Введите пароль от логина почты для отправки: ')+'\n')
    data.write(input('Введите ваш собственный API ключ разработчика Atlasian: ')+'\n')
    data.write(input('Введите ссылку на ваш проект: ')+'\n')

data_list = []
for i in data:
    data_list.append(i)
data.close()

emps = []
mails = open('adress.csv') 
c = csv.reader(mails)
for row in c:
    try:
        emps.append(row[0])
        if row[0].split('@')[1] != 'dengisrazy.ru' :
            raise MailException('Почта исполнителя некорректного формата')
    except Exception :
        print()

mails.close()
now = date.today()
date1 = date(now.year,now.month,(now.day-2))
date2 = date(now.year,now.month,(now.day-1))
jiraOptions = {'server': data_list[3]} 
jira = JIRA(options=jiraOptions, basic_auth=("mail.for.testbase@gmail.com", data_list[2])) 

for i in emps :
    inTwoDays = jira.search_issues('assignee = "'+i+'"and (status = "In Progress" or status = "To Do") and duedate = '+str(date1)+' order by created desc', fields=['summary'])
    inOneDay = jira.search_issues('assignee = "'+i+'"and (status = "In Progress" or status = "To Do") and duedate = '+str(date2)+' order by created desc', fields=['summary'])
    today = jira.search_issues('assignee = "'+i+'"and (status = "In Progress" or status = "To Do") and duedate = '+str(now)+' order by created desc', fields=['summary'])

with open('samp1.txt', 'r') as f1:
    sendOneDay = f1.read()
with open('samp2.txt', 'r') as f2:
    sendTwoDays = f2.read()
with open('samp0.txt', 'r') as f0:
    sendToday = f0.read()

if len(inTwoDays) != 0 :
    for j in inTwoDays:
        sendTwoDays += j.fields.summary

if len(inOneDay) != 0 :
    for j in inOneDay:
        sendOneDay += j.fields.summary

if len(today) != 0 :
    for j in today:
        sendToday += j.fields.summary

value = [sendTwoDays, sendOneDay, sendToday]   
for i in value:
    for j in emps:
        mail_send(str(i),'fox228sasha@mail.ru',data_list[0],data_list[1])